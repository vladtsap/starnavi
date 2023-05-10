from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view


@api_view(['GET'])
def hello_world(request):
    return JsonResponse({'message': 'Hello, world!'})
