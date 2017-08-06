from django.conf import settings

api_settings = settings.REST_FRAMEWORK

class APIViewPaginationMixin(object):

    paginator = api_settings['DEFAULT_PAGINATION_CLASS']

    def paginate_queryset(self, queryset, request, view=None):
        print 'paginating'
        return self.paginator.paginate_queryset(queryset, request, view)



