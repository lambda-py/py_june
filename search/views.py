from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from posts.models import Post


def search(request: HttpRequest) -> HttpResponse:
    search_text = request.GET.get("search", "")
    if len(search_text) == 0 or not search_text[0].isalpha():
        query = None
    else:
        query = Post.objects.filter(title__icontains=search_text).order_by(
            "-updated_at"
        )
    return render(request, "ui/header/search_results.html", {"query": query})
