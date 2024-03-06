"""
URL configuration for py_june project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("core.urls")),
    path("forum/", include("categories.urls")),
    path("posts/", include("posts.urls")),
    path("comments/", include("comments.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("profile/", include("profiles.urls")),
    path("search/", include("search.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    prefix_default_language=False,
)
