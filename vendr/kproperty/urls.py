from django.conf.urls import url
from . import views

urlpatterns = [

        # Property views.
        url(r'^$', views.PropertyList.as_view()),
        url(r'^(?P<pk>[0-9+]+)/$', views.PropertyDetail.as_view()),

        # Property Field views.
        url(r'^(?P<pk>[0-9+]+)/features/$', views.FeaturesList.as_view()),
        url(r'^(?P<pk>[0-9+]+)/features/(?P<ft_pk>[0-9+]+)/$',
            views.FeaturesDetail.as_view()),

        url(r'^(?P<pk>[0-9+]+)/taxrecords/$', views.TaxRecordsList.as_view()),
        url(r'^(?P<pk>[0-9+]+)/taxrecords/(?P<tr_pk>[0-9+]+)/$',
            views.TaxRecordsDetail.as_view()),

        url(r'^(?P<pk>[0-9+]+)/images/$', views.ImagesList.as_view()),
        url(r'^(?P<pk>[0-9+]+)/images/(?P<i_pk>[0-9+]+)/$',
            views.ImagesDetail.as_view()),

        # Open house views.
        url(r'^(?P<pk>[0-9+]+)/openhouses/$', views.OpenHouseList.as_view()),
        url(r'^(?P<pk>[0-9+]+)/openhouses/(?P<oh_pk>[0-9a-f-]+)/$',
            views.OpenHouseDetail.as_view()),
        
        # RSVP view.
        url(r'^(?P<pk>[0-9+]+)/openhouses/(?P<oh_pk>[0-9a-f-]+)/rsvp/$',
            views.RSVPList.as_view()),
        url(r'^(?P<pk>[0-9+]+)/openhouses/(?P<oh_pk>[0-9a-f-]+)'
                             '/rsvp/(?P<rsvp_pk>[0-9a-f-]+)/$',
            views.RSVPDetail.as_view())
]

