import os

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View

from comments.models import Comment
from posts.models import Post
from subscription.forms import SubscriptionForm
from subscription.models import Subscription
from subscription.views import SubscriptionManager
from users.models import ForumUser

from .forms import EditAvatarProfileForm, EditProfileForm, EditProfileLinksForm
from .models import Profile


class ProfileView(LoginRequiredMixin, View):
    template_name = "profiles/profile.html"

    def get(self, request: HttpRequest, profile: str) -> HttpResponse:
        user = get_object_or_404(ForumUser, username=profile)
        profile, create = Profile.objects.get_or_create(user=self.request.user)

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
        return render(
            request,
            self.template_name,
            {"user": user, "profile": profile, "context": context},
        )


class EditProfileView(UserPassesTestMixin, View):
    template_name = "profiles/edit_profile.html"

    def test_func(self) -> bool:
        profile_slug = self.kwargs.get("profile")
        profile = get_object_or_404(ForumUser, username=profile_slug)
        return profile.username == self.request.user.username

    def get(self, request: HttpRequest, profile: str) -> HttpResponse:
        user = get_object_or_404(ForumUser, username=profile)
        edit_profile_form = EditProfileForm(instance=user)
        user_profile = get_object_or_404(Profile, user=self.request.user)
        edit_links_form = EditProfileLinksForm(instance=user_profile)
        edit_avatar_form = EditAvatarProfileForm(instance=user)

        user_subscriptions = Subscription.objects.get(user=user)
        subscription_form = SubscriptionForm(user=user, instance=user_subscriptions)

        return render(
            request,
            self.template_name,
            {
                "user": user,
                "edit_profile_form": edit_profile_form,
                "edit_links_form": edit_links_form,
                "edit_avatar_form": edit_avatar_form,
                "subscription_form": subscription_form,
            },
        )

    def post(self, request: HttpRequest, profile: str) -> HttpResponse:
        user = get_object_or_404(ForumUser, username=profile)
        edit_profile_form = EditProfileForm(request.POST, instance=user)
        user_profile = get_object_or_404(Profile, user=self.request.user)
        edit_links_form = EditProfileLinksForm(request.POST, instance=user_profile)
        edit_avatar_form = EditAvatarProfileForm(
            request.POST, request.FILES, instance=user
        )
        current_avatar = user.avatar
        subscription_form = SubscriptionForm(request.POST, user=request.user)

        if current_avatar and "avatar" in request.FILES:
            if current_avatar != request.FILES["avatar"]:
                os.remove(current_avatar.path)

        if (
            edit_profile_form.is_valid()
            and edit_links_form.is_valid()
            and edit_avatar_form.is_valid()
            and subscription_form.is_valid()
        ):
            user_profile = edit_profile_form.save(commit=False)
            user_links = edit_links_form.save(commit=False)
            user_subscribe = subscription_form.save(commit=False)
            user_profile.user = self.request.user
            user_profile.avatar = edit_avatar_form.cleaned_data["avatar"]
            subscription_form.instance.user = request.user

            subscription_manager = SubscriptionManager(user)
            selected_categories = subscription_form.cleaned_data["categories"]
            subscription_manager.update_subscriptions(selected_categories, user)

            user_profile.save()
            user_links.save()
            user_subscribe.save()
            messages.success(request, _("Profile was updated successfully"))
            return redirect("profile:profile", profile=self.request.user.username)

        return render(
            request,
            self.template_name,
            {
                "edit_profile_form": edit_profile_form,
                "edit_links_form": edit_links_form,
                "edit_avatar_form": edit_avatar_form,
                "subscription_form": subscription_form,
                "user": user,
            },
        )
