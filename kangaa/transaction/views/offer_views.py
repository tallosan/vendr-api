from django.contrib.auth import get_user_model
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import generics, status, permissions

from kproperty.models import Property

from transaction.models import Transaction, Offer
from transaction.serializers import OfferSerializer
from transaction.permissions import TransactionAccessPermission

User = get_user_model()


'''   Offer list view. '''
class OfferList(APIView):

    serializer_class   = OfferSerializer
    permission_classes = ( permissions.IsAuthenticated, )

    ''' Custom 'get_queryset()' method to get only Offer models involved in
        the given transaction.
        Args:
            transaction_pk: The primary key of the Transaction we're querying over.
    '''
    def get_queryset(self, transaction_pk):

        transaction = Transaction.objects.get(pk=transaction_pk)
        return transaction.offers.all()

    ''' Get a list of offers associated with a given transaction.
        Args:
            request: Handler for request field.
            transaction_pk: The primary key of the Transaction we're querying over.
            *format: Specified data format.
    '''
    def get(self, request, transaction_pk, format=None):
        
        queryset = self.get_queryset(transaction_pk)

        response = []
        for offer in queryset:
            response.append(self.serializer_class(offer).data)
        
        return Response(response)
        
    ''' Create a new Offer for the given transaction.
        Args:
            request: The POST request.
            transaction_pk: The primary key of the Transaction we're querying over.
            *format: Specified data format.
    '''
    def post(self, request, transaction_pk, format=None):
        
        # Create the new Offer and link it to the given transaction.
        serializer  = self.serializer_class(data=request.data)
        transaction = Transaction.objects.get(pk=transaction_pk)
        
        if serializer.is_valid():
            serializer.save(owner=self.request.user, transaction=transaction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''   Offer detail view. '''
class OfferDetail(APIView):

    serializer_class   = OfferSerializer
    permission_classes = (
                            permissions.IsAuthenticated,
                            TransactionAccessPermission,
    )

    ''' Get the transaction model if the user has the requisite permissions.
        Args:
            transaction_pk: The primary key of the transactoin this offer belongs to.
            pk: The primary key of the Offer.
    '''
    def get_object(self, transaction_pk, pk):
        
        # Get the offer by filtering through the list of offers associated with the
        # given transaction. This ensures we aren't accessing external offers.
        try:
            transaction = Transaction.objects.get(pk=transaction_pk)
            offer = transaction.offers.all().get(pk=pk)
            
            return offer

        # Determine exception, and return an appropriate custom error message.
        except (Transaction.DoesNotExist, Offer.DoesNotExist) as dne_exception:
            if type(dne_exception) == Transaction.DoesNotExist:
                error_resource = 'transaction'
                error_pk = str(transaction_pk)
            else:
                error_resource = 'offer'
                error_pk = str(pk)

            error_msg = {'error': error_resource + ' with id ' + error_pk + \
                                  ' does not exist.'}
            dne_exc = APIException(detail=error_msg)
            dne_exc.status = status.HTTP_400_BAD_REQUEST
            
            raise dne_exc

    ''' Handles GET requests for Offer models.
        Args:
            request: Handler for the request field.
            pk: The primary key of the transaction.
            *format: Specified data format (e.g. JSON).
    '''
    def get(self, request, transaction_pk, pk, format=None):

        offer = self.get_object(transaction_pk=transaction_pk, pk=pk)
        serializer = self.serializer_class(offer)
        
        return Response(serializer.data)

