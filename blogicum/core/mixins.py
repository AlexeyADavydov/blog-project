from blog.models import Comment, Post
from blog.forms import PostForm
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse


class CommentUpdateDeleteMixinView(LoginRequiredMixin, View):
    model = Comment
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        get_object_or_404(Comment,
                          pk=kwargs['comment_id'],
                          author=request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'pk': self.kwargs['pk']})

    def get_object(self):
        comment = get_object_or_404(Comment, pk=self.kwargs['comment_id'])
        return comment


class PostUpdateDeleteMixinView(LoginRequiredMixin, View):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
