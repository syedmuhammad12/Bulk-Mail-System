from django.contrib import admin
from django.urls import path, include
from bulk_mail import views

urlpatterns = [
    path('', views.index, name="index"),
    path('send', views.sendemail, name="sendmail"),
]