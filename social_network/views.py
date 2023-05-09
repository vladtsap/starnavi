from django.http import HttpResponse, JsonResponse


def hello_world(request):
    return JsonResponse({'message': 'Hello, world!'})
