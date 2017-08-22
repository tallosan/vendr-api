#
# Contract views.
#
# ===========================================================================

from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status, permissions

from transaction.models import Transaction, Contract, StaticClause, DynamicClause
from transaction.serializers import ContractSerializer, StaticClauseSerializer
from transaction.exceptions import BadTransactionRequest
import transaction.permissions as transaction_permissions

import transaction.serializers as serializers

User = get_user_model()


'''   Contract list view. '''
class ContractList(APIView):

    serializer_class = ContractSerializer
    permission_classes = ( permissions.IsAuthenticated,
                           transaction_permissions.TransactionMemberPermission
    )
   
    ''' Returns a tuple of the transaction, and the actual contracts being queryed.
        Args:
            transaction_pk: The primary key of the transaction we're querying over.
    '''
    def get_queryset(self, transaction_pk):

        transaction = Transaction.objects.get(pk=transaction_pk)
        self.check_object_permissions(self.request, transaction)

        return transaction.contracts.all()
   
    ''' Handles LIST / GET requests.
        Args:
            request: The GET request.
            transaction_pk: The primary key of the transaction we're querying over.
            *format: Specified data format.
    '''
    def get(self, request, transaction_pk, format=None):
        
        queryset = self.get_queryset(transaction_pk)

        response = []
        for contract in queryset:
            response.append(self.serializer_class(contract).data)

        return Response(response)

    ''' Handles POST requests.
        Args:
            request: The POST request.
            transaction_pk: The primary key of the transaction we're querying over.
            *format: Specified data format.
    '''
    def post(self, request, transaction_pk, format=None):
        
        # Get the contract type.
        try:
            ctype = request.data.pop('ctype')
            valid_contract_types = ['coop', 'condo', 'house', 'townhouse', \
                    'manufactured', 'vacant_land']
            if ctype not in valid_contract_types:
                error_msg = {'error': 'invalid ctype {}'.format(ctype) }
                raise BadTransactionRequest(error_msg)
        except KeyError:
            error_msg = {'error': 'contract type must be specified! none given.'}
            raise BadTransactionRequest(error_msg)
        
        transaction = Transaction.objects.get(pk=transaction_pk)
        self.check_object_permissions(self.request, transaction)

        serializer  = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user, transaction=transaction, ctype=ctype)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''   Contract detail view. '''
class ContractDetail(APIView):

    serializer_class = ContractSerializer
    permission_classes = (
                            permissions.IsAuthenticated,
                            transaction_permissions.ContractDetailPermissions
    )

    ''' Return the Contract object if it exists.
        Args:
            transaction_pk: The transaction that the contract belongs to.
            pk: The primary key of the contract.
    '''
    def get_object(self, transaction_pk, pk):
        
        try:
            transaction = Transaction.objects.get(pk=transaction_pk)
            contract = transaction.contracts.get(pk=pk)
            self.check_object_permissions(self.request, contract)
            
            return contract
        except Contract.DoesNotExist:
            error_msg = {'error': 'contract with pk {} does not exist.'}.\
                         format(pk)
            raise BadTransactionRequest(error_msg)

    ''' Handles GET requests on Contract models.
        Args:
            request: The GET request.
            transaction_pk: The transaction that the contract belongs to.
            pk: The primary key of the contract to get.
            *format: Specified data format (e.g. JSON).
    '''
    def get(self, request, transaction_pk, pk, format=None):
        
        contract = self.get_object(transaction_pk, pk)
        serializer = self.serializer_class(contract)

        return Response(serializer.data)
   
    ''' Handles DELETE requests on Contract models.
        Args:
            request: The DELETE request.
            transaction_pk: The transaction that the contract belongs to.
            pk: The primary key of the contract to delete.
            *format: Specified data format (e.g. JSON).
    '''
    def delete(self, request, transaction_pk, pk, format=None):
        
        contract = self.get_object(transaction_pk, pk)
        contract.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

# ============================================================================
# Clause Views.

def resolve_serializer(serializer_class):
    return getattr(serializers, serializer_class)


'''   Clause list view. '''
class ClauseList(APIView):

    permission_classes = ( permissions.IsAuthenticated,
                           transaction_permissions.TransactionMemberPermission
    )

    ''' Returns a set of clauses belonging to the given transaction and contract.
        Args:
            transaction_pk: The primary key of the transaction we're querying over.
            contract_pk: The primary key of the contract we're querying over.
    '''
    def get_queryset(self, transaction_pk, contract_pk):

        transaction = Transaction.objects.get(pk=transaction_pk)
        self.check_object_permissions(self.request, transaction)

        contract = transaction.contracts.get(pk=contract_pk)

        return contract.clauses

    ''' Handles LIST / GET requests.
        Args:
            request: The GET request.
            transaction_pk: The primary key of the transaction we're querying over.
            contract_pk: The primary key of the contract we're querying over.
            *format: Specified data format.
    '''
    def get(self, request, transaction_pk, contract_pk, format=None):
        
        queryset = self.get_queryset(transaction_pk, contract_pk)
        
        # Serialize static and dynamic clauses.
        static_clauses = []; dynamic_clauses = []
        for clause in queryset:
            serializer = resolve_serializer(clause.serializer)
            
            if type(clause) is StaticClause:
                static_clauses.append(serializer(clause).data)
            else:
                dynamic_clauses.append(serializer(clause).data)

        response = {
                        'static_clauses': static_clauses,
                        'dynamic_clauses': dynamic_clauses
        }
        
        return Response(response)

    ''' Handles POST requests.
        Args:
            request: The POST request.
            transaction_pk: The primary key of the transaction we're querying over.
            contract_pk: The primary key of the contract we're querying over.
            *format: Specified data format.
    '''
    def post(self, request, transaction_pk, contract_pk, format=None):
        
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


'''   Clause detail view. '''
class ClauseDetail(APIView):

    serializer_class = None
    permission_classes = ( permissions.IsAuthenticated,
                           transaction_permissions.ClauseDetailPermissions
    )

    ''' Return the Clause object if it exists.
        Args:
            transaction_pk: The transaction that the contract belongs to.
            pk: The primary key of the contract.
    '''
    def get_object(self, transaction_pk, contract_pk, pk):
        
        transaction = Transaction.objects.get(pk=transaction_pk)
        contract = transaction.contracts.get(pk=contract_pk)
        
        # Attempt to get the clause in our static & dynamic sets respectively.
        try:
            clause = contract.static_clauses.get(pk=pk)
        except StaticClause.DoesNotExist:
            clause = contract.dynamic_clauses.get(pk=pk).actual_type
        except DynamicClause.DoesNotExist:
            error_msg = {'error': 'clause with pk {} does not exist.'}.\
                         format(pk)
            raise BadTransactionRequest(error_msg)
        
        self.check_object_permissions(self.request, clause)
        self.serializer_class = resolve_serializer(clause.serializer)

        return clause

    ''' Handles GET requests on Clause models.
        Args:
            request: The GET request.
            transaction_pk: The transaction that the clause contract belongs to.
            contract_pk: The primary key of the contract the clause belongs to.
            clause_pk: The primary key of the clause we're retrieving.
            pk: The primary key of the clause to get.
            *format: Specified data format (e.g. JSON).
    '''
    def get(self, request, transaction_pk, contract_pk, pk, format=None):
        
        clause = self.get_object(transaction_pk, contract_pk, pk)
        serializer = self.serializer_class(clause)
        
        return Response(serializer.data)
    
    ''' Handles PUT requests on Clause models.
        Args:
            request: The PUT request.
            transaction_pk: The transaction that the clause contract belongs to.
            contract_pk: The primary key of the contract the clause belongs to.
            pk: The primary key of the clause to update.
            *format: Specified data format (e.g. JSON).
    '''
    def put(self, request, transaction_pk, contract_pk, pk, format=None):
        
        clause = self.get_object(transaction_pk, contract_pk, pk)
        serializer = self.serializer_class(clause, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    ''' Handles DELETE requests on Clause models.
        Args:
            request: The DELETE request.
            transaction_pk: The transaction that the clause contract belongs to.
            contract_pk: The primary key of the contract the clause belongs to.
            pk: The primary key of the clause to delete.
            *format: Specified data format (e.g. JSON).
    '''
    def delete(self, request, transaction_pk, contract_pk, pk, format=None):
        
        clause = self.get_object(transaction_pk, contract_pk, pk)
        clause.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

