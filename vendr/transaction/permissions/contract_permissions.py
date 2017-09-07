#
# Custom permissions on Contract and Clause models.
# models (Offers and Contracts).
#
# ==============================================================================

from rest_framework import permissions


class ContractDetailPermissions(permissions.BasePermission):

    """ Transaction participants can read any offer. However, only the offer
        owner can delete it. """
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


class ClauseDetailPermissions(permissions.BasePermission):

    """ Transaction participants can read any offer. However, only the offer
        owner can delete it. """
    def has_object_permission(self, request, view, clause):

        # Any transaction participant can read offers.
        transaction = clause.contract.transaction
        if request.user not in [transaction.buyer, transaction.seller]:
            return False

        # Ensure that the user actually owns the offer.
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user == clause.contract.owner

