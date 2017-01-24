from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.PropertyList.as_view()),
        url(r'^(?P<pk>[0-9+]+)/$', views.PropertyDetail.as_view()),
]

