#
# Custom permissions on Offer models.
#
# ==============================================================================

from rest_framework import permissions


class OfferDetailPermissions(permissions.BasePermission):

    """ Transaction participants can read any offer. However, only the offer
        owner can delete it. """
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

