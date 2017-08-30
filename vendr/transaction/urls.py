from django.conf.urls import url
from . import views

urlpatterns = [
        
        # Transaction views.
        url(r'^$', views.TransactionList.as_view()),
        url(r'^(?P<transaction_pk>[0-9a-f-]+)/$', views.TransactionDetail.as_view()),
 
        # Advance Stage.
        url(r'^(?P<transaction_pk>[0-9a-f-]+)/advance/$',
            views.AdvanceStageList.as_view()),

        # Offer views.
        url(r'^(?P<transaction_pk>[0-9a-f-]+)/offers/$', views.OfferList.as_view()),
        url(r'^(?P<transaction_pk>[0-9a-f-]+)/offers/(?P<pk>[0-9a-f-]+)/$',
            views.OfferDetail.as_view()),

        # Contract views.
        url(r'^(?P<transaction_pk>[0-9a-f-]+)/contracts/$',
            views.ContractList.as_view()),
        url(r'^(?P<transaction_pk>[0-9a-f-]+)/contracts/(?P<pk>[0-9a-f-]+)/$',
            views.ContractDetail.as_view()),

        # [Contract] :: Clause views.
        url(r'^(?P<transaction_pk>[0-9a-f-]+)/contracts/(?P<contract_pk>[0-9a-f-]+)/'
                'clauses/$',
            views.ClauseList.as_view(), name='clause-list'),
        url(r'^(?P<transaction_pk>[0-9a-f-]+)/contracts/(?P<contract_pk>[0-9a-f-]+)/'
                'clauses/(?P<pk>[0-9a-f-]+)/$',
            views.ClauseDetail.as_view()),

        # Closing views.
        url(r'^(?P<transaction_pk>[0-9a-f-]+)/closing/$',
            views.ClosingList.as_view()),
        url(r'^(?P<transaction_pk>[0-9a-f-]+)/closing/(?P<closing_pk>[0-9a-f-]+)/$',
            views.ClosingDetail.as_view()),
        url(r'^(?P<transaction_pk>[0-9a-f-]+)/closing/(?P<closing_pk>[0-9a-f-]+)/'
                'amendments/$',
            views.AmendmentsList.as_view()),
        url(r'^(?P<transaction_pk>[0-9a-f-]+)/closing/(?P<closing_pk>[0-9a-f-]+)/'
                'waiver/$',
            views.WaiverList.as_view()),
        url(r'^(?P<transaction_pk>[0-9a-f-]+)/closing/(?P<closing_pk>[0-9a-f-]+)/'
                'notice_of_fulfillments/$',
            views.NoticeOfFulfillmentList.as_view()),
        url(r'^(?P<transaction_pk>[0-9a-f-]+)/closing/(?P<closing_pk>[0-9a-f-]+)/'
                'mutual_release/$',
            views.MutualReleaseList.as_view())
]

