from django.conf.urls import url
from . import views

urlpatterns = [
        url(r"^$", views.PaymentList.as_view()),
        url(r"^(?P<payment_pk>[0-9a-f-]+)/$", views.PaymentDetail.as_view()),
        url(r"^(?P<payment_pk>[0-9a-f-]+)/deposit/$",
            views.PaymentDeposit.as_view()),
        url(r"^(?P<payment_pk>[0-9a-f-]+)/forward/$",
            views.PaymentForward.as_view()),
]

