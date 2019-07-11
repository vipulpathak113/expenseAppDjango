from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, re_path

from . import views
from . import PaymentViews

urlpatterns = [
    url(r'^sheet', views.SheetDetail.as_view()),
    url(r'^count', views.CountDetail.as_view()),
    url(r'^count/(?P<pk>\d+)$', views.CountDetail.as_view()),
    url(r'^count/delete/', views.CountDetail.as_view()),
    url(r'^payment', views.PaymentDetail.as_view()),
    url(r'^payment/(?P<pk>\d+)$', views.PaymentDetail.as_view()),
    url(r'^sheet/(?P<pk>\d+)$', views.SheetDetail.as_view()),
    url(r'^compute', PaymentViews.ComputePayment.as_view()),
    url(r'^compute/(?P<pk>\d+)$', PaymentViews.ComputePayment.as_view()),
    url(r'^compute/delete/', PaymentViews.ComputePayment.as_view()),
    url(r'^$', views.ExpenseDetail.as_view()),
    url(r'^sheet/delete/', views.SheetDetail.as_view()),
    url(r'^person', views.PersonDetail.as_view()),
    url(r'^person/(?P<pk>\d+)$', views.PersonDetail.as_view()),
    url(r'^person/delete/', views.PersonDetail.as_view()),
    url(r'^$', views.ExpenseDetail.as_view()),
    url(r'^(?P<pk>\d+)$', views.ExpenseDetail.as_view()),
    url(r'^delete/', views.ExpenseDetail.as_view()),
    url(r'^(?P<pk>\d+)&(?P<eid>\d+)$', views.ExpenseDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
