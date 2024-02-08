from django import template
from django.shortcuts import get_object_or_404, render

from comments.forms import CommentForm
from comments.models import Comment
from core.utils.get_comment_inst import get_comment_inst
from posts.models import Post

register = template.Library()


@register.inclusion_tag("comments/comment_update.html")
def render_comment_update_form(comment):
    edit_comment_form = CommentForm(instance=comment, content_id=5)  # type: ignore[arg-type]
    return {"edit_comment_form": edit_comment_form}
