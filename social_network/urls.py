from django.urls import path

from social_network import views

urlpatterns = [
    path('hello', views.hello_world),
]
