from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View

from posts.models import Post

from .models import Reactions


class ReactionsView(LoginRequiredMixin, View):
    template_name = "posts/post_detail.html"

    def get(self, request: HttpRequest, id:int) -> HttpResponse:
        post = get_object_or_404(Post, pk=id, is_active=True)
        return redirect("posts:details", post_slug=post.slug)

    def post(self, request: HttpRequest, id: int) -> HttpResponseRedirect:
        post = get_object_or_404(Post, pk=id, is_active=True)
        if not Reactions.objects.filter(
            post_id=post.id, user_id=self.request.user.id
        ).exists():
            Reactions.objects.create(user_id=self.request.user.id, post_id=post.id)
        else:
            Reactions.objects.filter(
                user_id=self.request.user.id, post_id=post.id
            ).delete()
        return HttpResponseRedirect(reverse("posts:details", args={post.slug}))
