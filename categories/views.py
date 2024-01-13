from django.core.paginator import Paginator
from django.db import models
from django.db.models import Count, OuterRef, Subquery
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from categories.models import Category, MainCategory
from comments.models import Comment
from posts.models import Post


def category_list(request: HttpRequest) -> HttpResponse:
    # FIXME: Probably not the best way to do this
    last_comment_subquery = (
        Comment.objects
        .filter(post__category=OuterRef("pk"))
        .select_related("author")
        .order_by("-created_at")
        .values("author__username")[:1]
    )

    categories = Category.objects.annotate(
        post_count=Count("posts", distinct=True),
        comment_count=Count("posts__comments", distinct=True),
        last_comment=Subquery(last_comment_subquery, output_field=models.CharField()),
    ).select_related("main_category")

    main_categories = MainCategory.objects.all()
    context = {
        "main_categories": main_categories,
        "categories": categories,
    }
    return render(request, "categories/category_list.html", context)


def category_detail(request: HttpRequest, category_slug: str) -> HttpResponse:
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category_id=category.id, is_active=True)
    paginator = Paginator(posts, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "categories/category_detail.html",
        {"page_obj": page_obj, "category": category},
    )
