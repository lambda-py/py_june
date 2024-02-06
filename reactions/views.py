from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import View
from django.urls import reverse

from posts.models import Post
from .models import Reactions

class ReactionsView(View):
    template_name = 'posts/post_detail.html'

    def post(self, request, id):
        post = get_object_or_404(Post, pk=id, is_active=True)
        if not Reactions.objects.filter(post_id=post.id, user_id=self.request.user.id).exists():
            Reactions.objects.create(user_id=self.request.user.id, post_id=post.id, slug=post.slug)
        else:
            Reactions.objects.filter(user_id=self.request.user.id, post_id=post.id, slug=post.slug).delete()
        return HttpResponseRedirect(reverse('posts:details', args={post.slug}))