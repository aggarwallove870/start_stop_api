
from django.contrib import admin
from django.urls import path, include
from accounts.views import views
from accounts.views import api_views

urlpatterns = [

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name= 'elogout'),
    path('registration/', views.registration, name='registration'),
    path('create/password/<secret>/', views.createpassword, name='create/password'),
#api views
    path('time-api', api_views.TimeTracker.as_view()),
    # path('start_and_stop/',api_views.time_user)

]
