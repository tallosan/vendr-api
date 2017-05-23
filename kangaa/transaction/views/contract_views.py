#
# Contract views.
#
# ===========================================================================

from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status, permissions

from transaction.models import Transaction
from transaction.serializers import ContractSerializer

User = get_user_model()


'''   Contract list view. '''
class ContractList(APIView):

    serializer_class = ContractSerializer
   
    ''' Returns a tuple of the transaction, and the actual contracts being queryed.
        Args:
            transaction_pk: The primary key of the transaction we're querying over.
    '''
    def get_queryset(self, transaction_pk):

        transaction = Transaction.objects.get(pk=transaction_pk)
        return transaction.contracts.all(), transaction
   
    ''' Handles LIST / GET requests.
        Args:
            request: The GET request.
            transaction_pk: The primary key of the transaction we're querying over.
            *format: Specified data format.
    '''
    def get(self, request, transaction_pk, format=None):
        
        queryset = self.get_queryset(transaction_pk)

        response = []
        for contract in queryset[0]:
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
        except KeyError:
            pass
        
        transaction = Transaction.objects.get(pk=transaction_pk)
        serializer  = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user, transaction=transaction, ctype=ctype)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''   Contract detail view. '''
class ContractDetail(APIView):

    ''' Return the Contract object if it exists.
        Args:
            transaction_pk: The transaction that the contract belongs to.
            pk: The primary key of the contract.
    '''
    def get_object(self, transaction_pk, pk):
        
        try:
            transaction = Transaction.objects.get(pk=transaction_pk)
            contract = transaction.contracts.get(pk=pk)

            # TODO: Check permissions here.
            return contract
        except Exception as ex:
            print str(ex)

    ''' Handles GET requests on Contract models.
        Args:
            request: The GET request.
            transaction_pk: The transaction that the contract belongs to.
            pk: The primary key of the contract to get.
            *format: Specified data format (e.g. JSON).
    '''
    def get(self, request, transaction_pk, pk, format=None):
        
        self.serializer = ContractSerializer
        contract = self.get_object(transaction_pk, pk)
        serializer = self.serializer(contract)

        return Response(serializer.data)
    
    ''' Handles PUT requests on Contract models.
        Args:
            request: The PUT request.
            transaction_pk: The transaction that the contract belongs to.
            pk: The primary key of the contract to update.
            *format: Specified data format (e.g. JSON).
    '''
    def put(self, request, transaction_pk, pk, format=None):
        pass
    
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

