from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, UpdateView

from users.models import ForumUser
from profiles.models import ProfileUser
from profiles.forms import ProfileForm

class CreateProfileView(LoginRequiredMixin, View):
    template_name = "users/profile.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        form = ProfileForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = ProfileForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.forum_user = self.request.user
            user.save()
            return redirect("home")

        return render(request, self.template_name, {"form": form})


class ProfiletView(View):
    template_name = "users/profile.html"

    def get(
        self, request: HttpRequest, profile_slug: str) -> HttpResponse:
        user = get_object_or_404(ForumUser, username=profile_slug)

        profile = ForumUser.objects.first()

        context = {
            'id':       profile.id,
            'username': profile.username,
            'bio':      profile.bio,
            'email':    profile.email,
            'join':     profile.date_joined,

        }
        return render(request, self.template_name, {"user": user, "context": context})

    def post(
        self, request: HttpRequest, profile_slug: str) -> HttpResponse:
        user = get_object_or_404(ForumUser)

        return redirect("profile", post_slug=user.slug)