#
# Custom permissions on Closing, and any other closing related, models.
#
# ==============================================================================

from rest_framework import permissions


class ClauseDocumentListPermissions(permissions.BasePermission):

    """ For a clause list view, any user can GET (list) and/or POST, so the
        only permission we need to enforce is that the user making the
        request is actually part of the Transaction.
        Args:
            clause_set_parent (Document) -- The Document the clauses belong to.
    """
    def has_object_permission(self, request, view, clause_set_parent):

        transaction = clause_set_parent.closing.transaction
        return request.user in [transaction.buyer, transaction.seller]


class ClauseDocumentDetailPermissions(permissions.BasePermission):

    """ Transaction participants can read any document's clause list. However,
        we need to enforce field level permissions to ensure that the
        `buyer_accepted` and `seller_accepted` fields are not changed by the
        wrong party. """
    def has_object_permission(self, request, view, clause):

        transaction = clause.document.closing.transaction
        if request.user not in [transaction.buyer, transaction.seller]:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        return self.has_field_permissions(clause, request.user, request.data.keys())

    """ Check the user's field permissions.
        Args:
            clause (DocumentClause) -- The document clause the user is accessing.
            user (User) -- The user making the request.
            fields (list) -- A list of fields (by name) that the user is changing.
    """
    def has_field_permissions(self, clause, user, fields):
        return clause.check_field_permissions(user.pk, fields)

