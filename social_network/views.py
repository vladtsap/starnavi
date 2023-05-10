from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from social_network.models import Post, Like
from social_network.serializers import UserSerializer, PostSerializer


@api_view(['GET'])
def hello_world(request):
    return JsonResponse({'message': 'Hello, world!'})


@api_view(['POST'])
def sign_up(request):
    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=400)

    user = serializer.save()
    return JsonResponse({'username': user.username}, status=200)


@api_view(['GET'])
def hello_world(request):
    return JsonResponse({'message': 'Hello, world!'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hello(request):
    user = request.user
    return JsonResponse({'message': f'Hello, {user.username}!'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_create(request):
    user = request.user

    serializer = PostSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=400)

    post = serializer.save(author=user)
    return JsonResponse({'id': post.id}, status=200)


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
