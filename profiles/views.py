from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View

from comments.models import Comment
from posts.models import Post
from users.models import ForumUser
import os

from .forms import EditAvatarProfileForm, EditProfileForm


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
        is_user_page = user == self.request.user

        context = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "birth_date": user.birth_date,
            "username": user.username,
            "bio": user.bio,
            "email": user.email,
            "join": user.date_joined,
            "posts_count": posts_count,
            "comments_count": comments_count,
            "posts": posts,
            "my_profile": is_user_page,
        }
        return render(request, self.template_name, {"user": user, "context": context})


class EditProfileView(UserPassesTestMixin, View):
    template_name = "profiles/edit_profile.html"

    def test_func(self) -> bool:
        profile_slug = self.kwargs.get("profile")
        profile = get_object_or_404(ForumUser, username=profile_slug)
        return profile.username == self.request.user.username

    def get(self, request: HttpRequest, profile: str) -> HttpResponse:
        user = get_object_or_404(ForumUser, username=profile)
        user_form = EditProfileForm(instance=user)
        avatar_form = EditAvatarProfileForm(instance=user)

        return render(
            request,
            self.template_name,
            {"user": user, "user_form": user_form, "avatar_form": avatar_form},
        )

    def post(self, request: HttpRequest, profile: str) -> HttpResponse:
        user = get_object_or_404(ForumUser, username=profile)

        user_form = EditProfileForm(request.POST, instance=user)
        avatar_form = EditAvatarProfileForm(request.POST, request.FILES, instance=user)

        current_avatar = user.avatar
        
        if current_avatar:
            if current_avatar != avatar_form.data:
                os.remove(str(current_avatar))

        if user_form.is_valid() and avatar_form.is_valid():
            user = user_form.save(commit=False)
            user.avatar = avatar_form.cleaned_data["avatar"]
            user.save()
            return redirect("profile:profile", profile=self.request.user.username)

        return render(
            request,
            self.template_name,
            {"user_form": user_form, "avatar_form": avatar_form, "user": user},
        )
