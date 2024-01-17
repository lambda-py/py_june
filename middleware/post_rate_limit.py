from django.http import HttpResponseForbidden
from django.utils import timezone


class PostRateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            last_post_time = user.last_post_time
            if last_post_time:
                time_diff = timezone.now() - last_post_time
                if time_diff.total_seconds() < 300:
                    return HttpResponseForbidden("You can only post every 5 minutes.")

        response = self.get_response(request)
        return response
