from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from posts.models import Post


def search(request: HttpRequest) -> HttpResponse:
    search_text = request.GET.get("q", "")

    query = Post.objects.filter(title__icontains=search_text).order_by("-updated_at")
    return render(request, "search/search_result.html", {"query": query})
