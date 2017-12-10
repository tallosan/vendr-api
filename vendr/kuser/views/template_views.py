#
# Contract template views.
#
# @author :: tallosan
# ================================================================

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from django.contrib.auth import get_user_model

from transaction.models import AbstractContractFactory
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

    def get(self, pk, template_pk, request, *args, **kwargs):
        """
        Retrieve a contract template.
        """
        pass

    def put(self, pk, template_pk, request, *args, **kwargs):
        """
        Update a contract template.
        """

    def delete(self, pk, template_pk, request, *args, **kwargs):
        """
        Delete a contract template.
        """

