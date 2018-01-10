#
# Custom models.
#
# @author :: tallosan
# ================================================================

from elasticsearch import Elasticsearch

from django.db import models
from django.conf import settings

es = Elasticsearch([settings.ES_CONFIG])


class IndexedModel(models.Model):
    """
    Custom model for models that require indexing functionality. Note,
    the core setup here is in the `_index_meta` property, which contains
    a persistant and immutable representation of our model's config.
    Fields:
        `_document_id` (int) -- The Elastic search index Id.
    """
    
    # Note, this is optional to keep the model validator happy.
    _document_id = models.CharField(
            max_length=32,
            null=True,
            blank=True
    )

    class Meta:
        abstract= True

    @property
    def _index_meta(self):
        """
        Contains a dictionary with the `_*` fields defined below.
        Fields:
            `_index` (str) -- The index this document will belong to.
            `_indexable` (list of str) -- A list of fields to index.
            `_doc_type` (str) -- The type of document.
        """
        raise NotImplementedError(
                "error: all indexable models must implement this."
        )

    def _create_or_update_index(self):
        """
        Creates (or updates) an index, and returns a boolean value
        that represents the result of the operation. Condensing these
        two operations into a single wrapping function makes sense
        here due to the way this method will be used going forwards.
        """


        # Ensure that all ES configs are initialized, and valid.
        _meta = self._index_meta
        assert _meta["_indexable"] and _meta["_doc_type"], (
                "error: the `_index_meta` property does not have an "
                "an entry for `_indexable`. nothing to index!"
        )
        assert _meta["_doc_type"], (
                "error: `_index_meta` property does not have the "
                "_doc_type` entry set. document type must "
                "be specified!"
        )

        model_cls = type(self)
        values = model_cls.objects.values(
                "pk",
                *_meta["_indexable"]
        ).get(id=self.pk)

        # Index (or re-index) the necessary values.
        if self._document_id == None:
            document_id = self._create(values, _meta)
        else:
            document_id = self._update(values, _meta)

        return document_id

    def _create(self, values, _meta):
        """
        Create a document in the given index.
        Args:
            `values` (dict) -- The values contained in the document.
            `_meta` (dict) -- Meta config for index.
        """

        response = es.index(
                index=_meta["_index"],
                doc_type=_meta["_doc_type"],
                body=values
        )

        return response["_id"]

    def _update(self, values, _meta):
        """
        Updates a document in the given index.
        Args:
            `values` (dict) -- The values contained in the document.
            `_meta` (dict) -- Meta config for index.
        """

        response = es.update(
                index=_meta["_index"],
                doc_type=_meta["_doc_type"],
                id=self._document_id,
                body={"doc": values}
        )

        return response["_id"]

    def _delete_index(self):
        """
        Remove this model's document from the index it belongs to.
        """

        _meta = self._index_meta
        response = es.delete(
                index=_meta["_index"],
                doc_type=_meta["_doc_type"],
                id=self._document_id
        )

        return response["result"] == "deleted"

    def save(self, *args, **kwargs):
        """
        We're overriding this to ensure that changes to this model type
        are always reflected in the indices, whether that means a newly
        created model (and a newly created index), or a recently updated
        model (and an recently updated index).
        """

        # We can't create any indices before the initial save because
        # the related model's fields won't be available. Thus, to get
        # around this we can keep track of the state, and do a second
        # save if the model is newly created.
        set_doc_id = True if self._state.adding else False

        super(IndexedModel, self).save(*args, **kwargs)
        self._document_id = self._create_or_update_index()
        if set_doc_id:
            super(IndexedModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        We're overriding this to ensure that any model deletions are
        subsequently reflected in our index.
        """

        self._delete_index()
        super(IndexedModel, self).delete(*args, **kwargs)

