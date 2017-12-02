from django.conf.urls import url
from . import views

urlpatterns = [
        url(r"^$", views.PaymentList.as_view()),
        url(r"^(?P<transaction_pk>[0-9a-f-]+)/$", views.PaymentDetail.as_view()),
]

