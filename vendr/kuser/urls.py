from django.conf.urls import url
from . import views

urlpatterns = [
        
        # User views.
        url(r'^$', views.UserList.as_view()),
        url(r'^(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),

        # Notification views.
        url(r'^(?P<user_pk>[0-9]+)/notifications/ws_auth/$', views.NotificationWSAuth.as_view()),
        url(r'^(?P<user_pk>[0-9]+)/notifications/$', views.NotificationList.as_view()),
        url(r'^(?P<user_pk>[0-9]+)/notifications/(?P<pk>[0-9a-f-]+)/$',
            views.NotificationDetail.as_view()),
]

