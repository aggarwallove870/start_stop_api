
from django.urls import path
from . import views

urlpatterns = [

    path('', views.stripe_payment, name='payment'),
    path('handlerequest/', views.handlerequest, name='handlerequest'),
    path('package-selection/', views.paytm_payment, name='paytm_payment'),
    path('discount-detail/', views.discount_detail, name='discount_detail'),
]