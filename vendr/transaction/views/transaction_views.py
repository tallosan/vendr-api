from django.contrib.auth import get_user_model
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import generics, status, permissions

from kproperty.models import Property

from transaction.models import Transaction
from transaction.serializers import TransactionSerializer
from transaction.permissions import TransactionAccessPermission

from transaction.exceptions import BadTransactionRequest

User = get_user_model()


'''   Transaction list view. '''
class TransactionList(APIView):

    queryset           = Transaction.objects.all()
    serializer_class   = TransactionSerializer
    permission_classes = ( permissions.IsAuthenticated, )

    ''' Create a new Transaction. '''
    def post(self, request, format=None):
        
        # Attempt to get the seller and property models.
        try:
            seller_id    = request.data.pop('seller')
            kproperty_id = request.data.pop('kproperty')
            seller       = User.objects.get(id=seller_id)
            kproperty    = Property.objects.get(id=kproperty_id)
        
        except KeyError:
            error_msg = {'error': 'seller and buyer fields must be specified.'}
            raise BadTransactionRequest(detail=error_msg)
    
        # Ensure that only one offer is being passed initially.
        if len(request.data.get('offers')) != 1:
            error_msg = {'error': 'more than one initial offer sent.'}
            raise BadTransactionRequest(detail=error_msg)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(buyer=self.request.user, seller=seller, kproperty=kproperty)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''   Transaction detail view. We will perform all permission handling here at
      the view level, as there is simply no need to allow bad requests to pass
      any further. On top of restricting access permissions, we also need to enforce
      model instance permissions. '''
class TransactionDetail(APIView):

    queryset           = Transaction.objects.all()
    serializer_class   = TransactionSerializer
    permission_classes = (
                            permissions.IsAuthenticated,
                            TransactionAccessPermission,
    )

    ''' Get the transaction model if the user has the requisite permissions.
        Args:
            transaction_pk: The primary key of the Transaction.
    '''
    def get_object(self, transaction_pk):
        
        # Attempt to get the Transaction if it exists. If an instance is found then
        # check model level and instance level permissions.
        try:
            transaction = Transaction.objects.get(pk=transaction_pk)
            self.check_object_permissions(self.request, transaction)
            
            return transaction
        except Transaction.DoesNotExist:
            error_msg = {'error': 'transaction with id ' + str(transaction_pk) + \
                                  ' does not exist.'}
            raise BadTransactionRequest(detail=error_msg)

    ''' Handles GET requests for Transaction models.
        Args:
            request: Handler for the request field.
            transaction_pk: The primary key of the transaction.
            *format: Specified data format (e.g. JSON).
    '''
    def get(self, request, transaction_pk, format=None):
        
        transaction = self.get_object(transaction_pk)
        serializer  = self.serializer_class(transaction)
        
        return Response(serializer.data)
       
    ''' Handles PUT requests for Transaction models.
        Args:
            request: The update data for the transaction.
            transaction_pk: The primary key of the transaction.
            *format: Specified data format (e.g. JSON).
    '''
    def put(self, request, transaction_pk, format=None):

        # Handle invalid nested updates.
        if request.data.get('offers') or request.data.get('contracts'):
            error_msg = { 'error': 'nested fields should be handled through ' +\
                                    'their respective endpoints, not transaction/.' }
            raise BadTransactionRequest(detail=error_msg)

        # Get the given transaction, and perform an update.
        transaction = self.get_object(transaction_pk)
        serializer  = self.serializer_class(transaction, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    ''' Handles DELETE requests for Transaction models.
        Args:
            request: Handler for the request field.
            transaction_pk: The primary key of the transaction.
            *format: Specified data format (e.g. JSON).
    '''
    def delete(self, request, transaction_pk, format=None):

        transaction = self.get_object(transaction_pk)
        transaction.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


'''   Advance Stage list view. '''
class AdvanceStageList(APIView):

    serializer_class   = TransactionSerializer
    permission_classes = ( permissions.IsAuthenticated,
                           TransactionAccessPermission
    )

    ''' Advance the Transaction stage if possible. '''
    def post(self, request, transaction_pk, format=None):

        transaction = Transaction.objects.get(pk=transaction_pk)
        self.check_object_permissions(self.request, transaction)

        # Attempt to advance the stage.
        try:
            transaction.advance_stage()
        except ValueError as value_error:
            error_msg = {'error': str(value_error)}
            raise BadTransactionRequest(detail=error_msg)
        
        response = { 'stage': transaction.stage }
        return Response(response, status=status.HTTP_200_OK)

