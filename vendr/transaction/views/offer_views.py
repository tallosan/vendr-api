from django.contrib.auth import get_user_model
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import generics, status, permissions

from kproperty.models import Property

from transaction.models import Transaction, Offer
from transaction.serializers import OfferSerializer
from transaction.exceptions import BadTransactionRequest

import transaction.permissions as transaction_permissions

User = get_user_model()


'''   Offer list view. '''
class OfferList(APIView):

    serializer_class   = OfferSerializer
    permission_classes = ( permissions.IsAuthenticated,
                           transaction_permissions.OfferListPermissions
    )

    ''' Custom 'get_queryset()' method to get only Offer models involved in
        the given transaction. Note, we separate the offers by their respective owners.
        Args:
            transaction_pk: The primary key of the Transaction we're querying over.
    '''
    def get_queryset(self, transaction_pk):

        transaction = Transaction.objects.get(pk=transaction_pk)
        self.check_object_permissions(self.request, transaction)
        
        return {
                'buyer_offers': transaction.get_offers(user_id=transaction.buyer),
                'seller_offers': transaction.get_offers(user_id=transaction.seller)
        }

    ''' Get a list of offers associated with a given transaction.
        Args:
            request: Handler for request field.
            transaction_pk: The primary key of the Transaction we're querying over.
            *format: Specified data format.
    '''
    def get(self, request, transaction_pk, format=None):
        
        queryset = self.get_queryset(transaction_pk)
        
        buyer_offers = self.serializer_class(queryset['buyer_offers'], many=True).data
        seller_offers = self.serializer_class(queryset['seller_offers'], many=True).data
        
        response = {
                        'buyer_offers': buyer_offers,
                        'seller_offers': seller_offers
        }
        
        return Response(response)
        
    ''' Create a new Offer for the given transaction.
        Args:
            request: The POST request.
            transaction_pk: The primary key of the Transaction we're querying over.
            *format: Specified data format.
    '''
    def post(self, request, transaction_pk, format=None):
        
        # Create the new Offer and link it to the given transaction.
        transaction = Transaction.objects.get(pk=transaction_pk)
        self.check_object_permissions(self.request, transaction)
        
        serializer  = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user, transaction=transaction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''   Offer detail view. '''
class OfferDetail(APIView):

    serializer_class   = OfferSerializer
    permission_classes = (
                            permissions.IsAuthenticated,
                            transaction_permissions.OfferDetailPermissions
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
            self.check_object_permissions(self.request, offer)
            
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
            raise BadTransactionRequest(detail=error_msg)

    ''' Handles GET requests for Offer models.
        Args:
            request: Handler for the request field.
            transaction_pk: The primary key of the transaction.
            pk: The primary key of the offer.
            *format: Specified data format (e.g. JSON).
    '''
    def get(self, request, transaction_pk, pk, format=None):

        offer = self.get_object(transaction_pk=transaction_pk, pk=pk)
        serializer = self.serializer_class(offer)
        
        return Response(serializer.data)

    ''' Handles DELETE requests for Offer models. Note, we can only delete the
        most recent offer.
        Args:
            request: The DELETE request.
            transaction_pk: The primary key of the transaction.
            pk: The primary key of the offer.
            *format: Specified data format (e.g. JSON).
    '''
    def delete(self, request, transaction_pk, pk, format=None):

        offer = self.get_object(transaction_pk=transaction_pk, pk=pk)

        # Ensure that the user both owns the offer, and the offer is the most recent.
        transaction = Transaction.objects.get(pk=transaction_pk)
        if offer != transaction.offers.filter(owner=request.user).latest('timestamp'):
            error_msg = {'error': 'only active (i.e. most recent) offers can be deleted.'}
            raise BadTransactionRequest(detail=error_msg)
        
        offer.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

