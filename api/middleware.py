from django.http import JsonResponse
from .models import APIToken

class APITokenMiddleware:
    """ Middleware to authenticate API requests using an APIToken """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only enforce API token check for API endpoints (paths starting with /api/)
        if request.path.startswith("/api/"):
            token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()

            if not APIToken.objects.filter(token=token).exists():
                return JsonResponse({"error": "Invalid API token"}, status=403)

        return self.get_response(request)