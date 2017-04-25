from django.conf.urls import url
from . import views

urlpatterns = [
        
        # Transaction views.
        url(r'^$', views.TransactionList.as_view()),
        url(r'^(?P<transaction_pk>[0-9a-f-]+)/$', views.TransactionDetail.as_view()),

        # Offer views.
        url(r'^(?P<transaction_pk>[0-9a-f-]+)/offers/$', views.OfferList.as_view()),
        url(r'^(?P<transaction_pk>[0-9a-f-]+)/offers/(?P<pk>[0-9a-f-]+)/$',
            views.OfferDetail.as_view()),

        # Contract views.
]

