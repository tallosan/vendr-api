#
# Contract template views.
#
# @author :: tallosan
# ================================================================

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import APIException

from django.contrib.auth import get_user_model

from transaction.models import AbstractContractFactory, Contract, StaticClause, DynamicClause
from transaction.serializers import GenericClauseSerializer, StaticClauseSerializer, \
        DynamicClauseSerializer, DropdownClauseSerializer
from kuser.serializers import TemplateContractSerializer

User = get_user_model()


class TemplateList(ListCreateAPIView):
    """
    List and create reusable contract templates.
    """

    queryset = User.objects.all()
    serializer_class = TemplateContractSerializer

    def get_queryset(self):
        """
        Return the contrac templates for the given user, specified by their pk.
        Args:
            `pk` (int) -- The user's pk.
        """
        
        user = self.queryset.get(pk=self.kwargs["pk"])
        return user.templates

    def post(self, request, *args, **kwargs):
        """
        Create a new contract template.
        """

        ctype = request.data.pop("ctype", None)
        owner = request.user

        # Explicitly add the `is_template` field to our request.
        request.data["is_template"] = True
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ctype=ctype, owner=owner)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TemplateDetail(RetrieveUpdateDestroyAPIView):
    """
    Get, update, and delete contract templates.
    """

    serializer_class = TemplateContractSerializer

    def get_object(self):
        """
        Get the contract template.
        """

        try:
            pk = self.kwargs["pk"]; template_pk = self.kwargs["template_pk"]
            kuser = User.objects.get(pk=pk)
            template = kuser.templates.get(pk=template_pk)
            return template
        except Contract.DoesNotExist:
            error_msg = {
                    "error": "contract template with pk {} does not exist".\
                            format(template_pk)
            }
            dne_exc = APIException(detail=error_msg)
            dne_exc.status_code = status.HTTP_400_BAD_REQUEST
            raise dne_exc
        

class TemplateClauseList(ListCreateAPIView):
    """
    List and create template clauses.
    """

    serializer_class = GenericClauseSerializer
    permission_classes = (
            permissions.IsAuthenticated,
    )

    def get_queryset(self):
        """
        Returns a set of clauses belonging to the given transaction and contract.
        Args:
            `transaction_pk` (UUID) -- The primary key of the transaction we're querying over.
            contract_pk: The primary key of the contract we're querying over.
        """

        user = User.objects.get(pk=self.kwargs["pk"])
        template = user.templates.get(pk=self.kwargs["template_pk"])
    
        queryset = {
                "static_clauses": template.static_clauses.all(),
                "dynamic_clauses": template.dynamic_clauses.all()
        }
        return queryset

    def get(self, request, *args, **kwargs):
        
        queryset = self.get_queryset()

        static_clauses = []
        for _clause in queryset["static_clauses"]:
            static_clauses.append(
                    self.get_serializer().to_representation(_clause)
            )

        dynamic_clauses = []
        for _clause in queryset["dynamic_clauses"]:
            dynamic_clauses.append(
                    self.get_serializer().to_representation(_clause)
            )
        response = {
                "static_clauses": static_clauses,
                "dynamic_clauses": dynamic_clauses
        }
        
        return Response(response)

    def post(self, request, *args, **kwargs):
        
        """
        # Get the contract type.
        try:
            ctype = request.data.pop('ctype')
        except KeyError:
            pass
        
        transaction = Transaction.objects.get(pk=transaction_pk)
        self.check_object_permissions(transaction, self.request)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user, transaction=transaction, ctype=ctype)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        """


class TemplateClauseDetail(RetrieveUpdateDestroyAPIView):
    """
    Template Clause detail view.
    """

    serializer_class = GenericClauseSerializer
    permission_classes = (
            permissions.IsAuthenticated,
    )

    def get_object(self, clause_pk=None):
        
        user = User.objects.get(pk=self.kwargs["pk"])
        template = user.templates.get(pk=self.kwargs["template_pk"])
        if not clause_pk:
            clause_pk = self.kwargs["clause_pk"]
        
        # Attempt to get the clause in our static & dynamic sets respectively.
        try:
            clause = template.static_clauses.get(pk=clause_pk)
        except StaticClause.DoesNotExist:
            clause = template.dynamic_clauses.get(pk=clause_pk).actual_type
        except DynamicClause.DoesNotExist:
            error_msg = {'error': 'clause with pk {} does not exist.'}.\
                         format(clause_pk)
            raise BadTransactionRequest(error_msg)
        
        self.check_object_permissions(self.request, clause)

        return clause
   

class TemplateClauseBatchDetail(TemplateClauseDetail):
    """
    Clause view for batch updates. Note, we're explicitly going to disallow
    any GET or DELETE requests.
    """

    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def put(self, request, *args, **kwargs):
        """
        Handles batch clause updates. Note, this is the only way we are handling
        these updates, as it allows us to minimize API requests, and connects
        better with our notifications API.
        """
        
        response = []
        for clause_data in request.data:
            pk = clause_data['pk']; data = clause_data['data']
            clause = self.get_object(clause_pk=pk)
            serializer_class = self._resolve_serializer(clause.serializer)
            serializer = serializer_class(
                    clause,
                    data=data,
                    partial=True
            )
            if serializer.is_valid():
                serializer.save()
                response.append(serializer.data)
            else:
                return Response(
                        serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(response)

    def delete(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def _resolve_serializer(self, serializer_class):
        """
        Resolve the serializer from the given serializer class.
        Args:
            `serializer_class` (str) -- The serializer class.
        """

        mapping = {
                "StaticSerializer": StaticClauseSerializer,
                "DynamicClauseSerializer": DynamicClauseSerializer,
                "DropdownClauseSerializer": DropdownClauseSerializer
        }

        return mapping[serializer_class]

