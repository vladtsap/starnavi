from datetime import datetime

from django.db import IntegrityError
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from social_network.models import Post, Like, SocialUser
from social_network.serializers import UserSerializer, PostSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        user = SocialUser.objects.get(username=request.data['username'])
        user.last_login = datetime.now()
        user.save()

        return response


@api_view(['GET'])
def hello_world(request):
    return JsonResponse({'message': 'Hello, world!'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hello(request):
    user = request.user
    return JsonResponse({'message': f'Hello, {user.username}!'})


@api_view(['POST'])
def sign_up(request):
    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=400)

    user = serializer.save()
    return JsonResponse({'username': user.username}, status=201)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_create(request):
    user = request.user

    serializer = PostSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=400)

    post = serializer.save(author=user)
    return JsonResponse({'id': post.id}, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_get(request, post_id: int):
    post = Post.objects.get(id=post_id)

    return JsonResponse(PostSerializer(post).data, status=200, safe=False)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def like_create_get_delete(request, post_id: int):
    post = Post.objects.get(id=post_id)

    if request.method == 'GET':
        likes = Like.objects.filter(post=post).count()
        return JsonResponse({'likes': likes}, status=200)

    elif request.method == 'POST':
        try:
            Like.objects.create(user=request.user, post=post)
        except IntegrityError:
            return JsonResponse({'message': 'You have already liked this post'}, status=400)
        else:
            return HttpResponse(status=200)

    elif request.method == 'DELETE':
        try:
            like = Like.objects.get(user=request.user, post=post)
        except Like.DoesNotExist:
            return JsonResponse({'message': 'You have not liked this post yet'}, status=400)
        else:
            like.delete()
            return HttpResponse(status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def analytics_for_user(request, user_id: int):
    user = SocialUser.objects.get(id=user_id)

    return JsonResponse({
        'username': user.username,
        'last_activity': user.last_activity,
        'last_login': user.last_login,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def analytics_for_likes(request):
    likes_per_day = Like.objects.annotate(date=TruncDate('made_at')).values('date').annotate(total_likes=Count('id'))
    likes_per_day = likes_per_day.order_by('date')

    if date_from := request.GET.get('date_from'):
        likes_per_day = likes_per_day.filter(date__gte=date_from)
    if date_to := request.GET.get('date_to'):
        likes_per_day = likes_per_day.filter(date__lte=date_to)

    result = [
        {'date': record['date'], 'total_likes': record['total_likes']}
        for record in likes_per_day
    ]
    return JsonResponse(result, safe=False)
