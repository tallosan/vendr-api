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
    Mixin for models that require indexing functionality. Note, the
    core setup here is in the `_index_meta` property, which contains
    a persistant and immutable representation of our model's config.
    Fields:
        `_document_id` (int) -- The Elastic search index Id.
    """
    
    _document_id = models.PositiveIntegerField(null=True, blank=True)

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
        that represents the result of the operation.
        """

        _meta = self._index_meta

        # Ensure that all ES configs are initialized, and valid.
        assert _meta["_indexable"] and _meta["_doc_type"], (
                "error: the `_index_meta` property does not have an "
                "an entry for `_indexable`. nothing to index!"
        )
        assert _meta["_doc_type"], (
                "error: `_index_meta` property does not have the "
                "_doc_type` entry set. document type must "
                "be specified!"
        )

        # Index the necessary values. Note, the elasticsearch-py
        # `index()` method will create or update by default, so we
        # don't need to work with this any more.
        model_cls = type(self)
        values = model_cls.objects.values(
                "pk",
                *_meta["_indexable"]
        ).get(id=self.pk)

        response = es.index(
                index=_meta["_index"],
                doc_type=_meta["_doc_type"],
                body=values
        )

        return response["result"] == "created"

    def _delete_index(self):
        """
        Remove this model's document from the index it belongs to.
        """

        es.delete(
                index=self._index,
                doc_type=self._doc_type,
                id=self._document_id
        )

        return es

    def save(self, *args, **kwargs):
        """
        We're overriding this to ensure that changes to this model type
        are always reflected in the indices, whether that means a newly
        created model (and a newly created index), or a recently updated
        model (and an recently updated index).
        """

        # TODO: Determine how to update, and route flow accordingly.
        super(IndexedModel, self).save(*args, **kwargs)
        #if self._state.adding:
            #create

        index_created = self._create_or_update_index()
        if not index_created:
            raise ValueError("error: index could not be created.")

    def delete(self, *args, **kwargs):
        """
        We're overriding this to ensure that any model deletions are
        subsequently reflected in our index.
        """

        super(IndexedModel, self).delete(*args, **kwargs)
        self._delete_index()

