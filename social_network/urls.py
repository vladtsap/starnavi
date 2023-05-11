from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from social_network import views
from social_network.views import CustomTokenObtainPairView

urlpatterns = [
    path('hello-world', views.hello_world),
    path('sign-up', views.sign_up),
    path('token', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('hello', views.hello),
    path('posts', views.create_post),
    path('posts/<int:post_id>', views.get_post),
    path('posts/<int:post_id>/like', views.like_create_get_delete),
    path('analytics/users/<int:user_id>', views.analytics_for_user),
    path('analytics/likes', views.analytics_for_likes),
]
