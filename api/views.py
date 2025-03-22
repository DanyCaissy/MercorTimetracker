from django.http import JsonResponse

def TestAuthentication(request):
    return JsonResponse({"message": "API call successful!"})