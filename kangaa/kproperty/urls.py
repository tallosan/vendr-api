from django.conf.urls import url
from . import views

urlpatterns = [

        # Property views.
        url(r'^$', views.PropertyList.as_view()),
        url(r'^(?P<pk>[0-9+]+)/$', views.PropertyDetail.as_view()),

        # Open house views.
        url(r'^(?P<pk>[0-9+]+)/openhouse/$', views.OpenHouseList.as_view()),
        url(r'^(?P<pk>[0-9+]+)/openhouse/(?P<oh_pk>[0-9a-f-]+)/$',
            views.OpenHouseDetail.as_view()),
        
        # RSVP view.
        url(r'^(?P<pk>[0-9+]+)/openhouse/(?P<oh_pk>[0-9a-f-]+)/rsvp/$',
            views.RSVPList.as_view()),
        url(r'^(?P<pk>[0-9+]+)/openhouse/(?P<oh_pk>[0-9a-f-]+)'
                             '/rsvp/(?P<rsvp_pk>[0-9a-f-]+)/$',
            views.RSVPDetail.as_view())
]

