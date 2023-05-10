from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from social_network import views

urlpatterns = [
    path('hello-world', views.hello_world),
    path('sign-up', views.sign_up),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('hello', views.hello),
    path('post', views.post_create_get),
    path('post/<int:post_id>/like', views.like_create_get_delete),
]
