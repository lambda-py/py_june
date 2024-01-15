from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, UpdateView

from comments.models import Comment
from posts.models import Post

# from profiles.forms import ProfileForm
from users.models import ForumUser

# TODO Pj-97 Create `settings` page for user

# class CreateProfileView(LoginRequiredMixin, View):
#     template_name = "users/profile.html"

#     def get(self, request: HttpRequest) -> HttpResponse:
#         form = ProfileForm()
#         return render(request, self.template_name, {"form": form})

#     def post(self, request: HttpRequest) -> HttpResponse:
#         form = ProfileForm(request.POST)

#         if form.is_valid():
#             user = form.save(commit=False)
#             user.forum_user = self.request.user
#             user.save()
#             return redirect("home")

#         return render(request, self.template_name, {"form": form})


class ProfiletView(LoginRequiredMixin, View):
    template_name = "users/profile.html"
    login_url = "/users/login/"

    def get(self, request: HttpRequest, profile: str) -> HttpResponse:
        user = get_object_or_404(ForumUser, username=profile)

        comments_count = Comment.objects.filter(author_id=user.id).count()
        posts_count = Post.objects.filter(author_id=user.id).count()

        context = {
            "id": user.id,
            "username": user.username,
            "bio": user.bio,
            "email": user.email,
            "join": user.date_joined,
            "posts_count": posts_count,
            "comments_count": comments_count,
        }
        return render(request, self.template_name, {"user": user, "context": context})

    def post(self, request: HttpRequest, profile_slug: str) -> HttpResponse:
        user = get_object_or_404(ForumUser)

        return redirect("profile", post_slug=user.slug)
