from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view

from social_network.serializers import UserSerializer


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
