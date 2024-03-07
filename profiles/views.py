from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, UpdateView

from categories.models import Category
from comments.models import Comment
from posts.models import Post

# from profiles.forms import ProfileForm
from users.models import ForumUser

# TODO Pj-97 Create `settings` page for user

# class CreateProfileView(LoginRequiredMixin, View):
#     template_name = "profiles/profile.html"

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


class ProfileView(LoginRequiredMixin, View):
    template_name = "profiles/profile.html"

    def get(self, request: HttpRequest, profile: str) -> HttpResponse:
        user = get_object_or_404(ForumUser, username=profile)

        comments_count = Comment.objects.filter(author_id=user.id).count()
        posts_count = Post.objects.filter(author_id=user.id).count()
        posts = (
            Post.objects.filter(author_id=user.id)
            .all()
            .annotate(post_comments_count=Count("comments"))
            .order_by("-created_at")
        )

        context = {
            "id": user.id,
            "username": user.username,
            "bio": user.bio,
            "email": user.email,
            "join": user.date_joined,
            "posts_count": posts_count,
            "comments_count": comments_count,
            "posts": posts,
        }
        return render(request, self.template_name, {"user": user, "context": context})
