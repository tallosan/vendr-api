#
# Custom permissions on Transaction models, and any related
# models (Offers and Contracts).
#
# ==============================================================================

from rest_framework import permissions


'''   Custom permission to handle object and field level access on Transactions. '''
class TransactionAccessPermission(permissions.BasePermission):
    
    ''' Determine whether or not the user has permission on the target model.
        If the request is safe (i.e. read-only), then we just need to ensure
        that the user belongs to the transaction. If not, then we'll need to
        check field permissions as well.
    '''
    def has_object_permission(self, request, view, transaction):
        
        # Ensure that the user belongs to the transaction.
        if request.user not in [transaction.buyer, transaction.seller]:
            return False
        
        # Determine if the request is safe. If not then we'll need to check
        # field level permissions.
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return self.has_field_permissions(request, transaction)

    ''' Determine whether or not the user has permission on every field that
        they are attempting to change.
    '''
    def has_field_permissions(self, request, transaction):
        
        return transaction.check_field_permissions(request.user.id, request.data)


class TransactionMemberPermission(permissions.BasePermission):

    ''' Ensure that the user is part of the transaction. '''
    def has_object_permission(self, request, view, transaction):

        return request.user in [transaction.buyer, transaction.seller]


class OfferDetailPermissions(permissions.BasePermission):

    ''' Transaction participants can read any offer. However, only the offer
        owner can delete it. '''
    def has_object_permission(self, request, view, offer):

        # Any transaction participant can read offers.
        transaction = offer.transaction
        if request.user not in [transaction.buyer, transaction.seller]:
            return False

        # Ensure that the user actually owns the offer.
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user == offer.owner


class ContractDetailPermissions(permissions.BasePermission):

    ''' Transaction participants can read any offer. However, only the offer
        owner can delete it. '''
    def has_object_permission(self, request, view, contract):

        # Any transaction participant can read offers.
        transaction = contract.transaction
        if request.user not in [transaction.buyer, transaction.seller]:
            return False

        # Ensure that the user actually owns the offer.
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user == contract.owner

