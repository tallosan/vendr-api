from django.conf.urls import url
from . import views

urlpatterns = [
        
        # User views.
        url(r'^$', views.UserList.as_view()),
        url(r'^(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),

        # Websocket Authentication.
        url(r'^(?P<pk>[0-9]+)/ws_auth/$', views.WSAuth.as_view()),

        # Two-Factor Authentication.
        url(r'^(?P<pk>[0-9]+)/two-factor-auth/$', views.TwoFactorAuth.as_view()),

        # Notification views.
        url(r'^(?P<user_pk>[0-9]+)/notifications/$', views.NotificationList.as_view()),
        url(r'^(?P<user_pk>[0-9]+)/notifications/(?P<pk>[0-9a-f-]+)/$',
            views.NotificationDetail.as_view()),

        # Chat views.
        url(r'^(?P<pk>[0-9]+)/chat/$', views.ChatList.as_view()),
        url(r'^(?P<pk>[0-9]+)/chat/(?P<chat_pk>[0-9a-f-]+)/$',
            views.ChatDetail.as_view()),
        url(r'^(?P<pk>[0-9]+)/chat/(?P<chat_pk>[0-9a-f-]+)/messages/$',
            views.MessageList.as_view()),
        
        # Schedule view.
        url(r'^(?P<pk>[0-9]+)/schedule/$', views.ScheduleList.as_view()),

        # Profile view.
        url(r'^(?P<pk>[0-9]+)/profile/$', views.ProfileDetail.as_view()),

        # Favourites view.
        url(r'^(?P<pk>[0-9]+)/subscriptions/$', views.SubscriptionsList.as_view()),

        # Property, Transaction, Contract, and Closing views.
        url(r'^(?P<pk>[0-9]+)/properties/$', views.PropertyList.as_view()),
        url(r'^(?P<pk>[0-9]+)/transactions/$', views.TransactionList.as_view()),
        url(r'^(?P<pk>[0-9]+)/contracts/$', views.ContractList.as_view()),
        url(r'^(?P<pk>[0-9]+)/closing/$', views.ClosingList.as_view()),
]

