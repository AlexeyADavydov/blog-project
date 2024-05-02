from django.shortcuts import get_object_or_404, redirect
from datetime import datetime
from .models import Post, Category, Comment
from django.contrib.auth.models import User
from .forms import PostForm, ProfileForm, CommentForm
from django.urls import reverse_lazy
from django.views.generic import (DetailView,
                                  ListView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView,)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.db.models import Count
from core.mixins import CommentUpdateDeleteMixinView, PostUpdateDeleteMixinView

NUM_OF_PUB_ON_PAGE: int = 10


class IndexListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = 10

    queryset = Post.objects.select_related(
        'author',
        'location',
        'category',
    ).order_by(
        '-pub_date',
    ).filter(
        pub_date__lte=datetime.now(),
        is_published=True,
        category__is_published=True,
    ).annotate(
        comment_count=Count('comments')
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_count'] = self.queryset.count()
        return context


class CategoryListView(ListView):
    model = Post
    template_name = 'blog/category.html'
    ordering = '-pub_date'
    paginate_by = NUM_OF_PUB_ON_PAGE

    def get_queryset(self):
        self.slug = get_object_or_404(
            Category,
            slug=self.kwargs['slug'],
            is_published=True,
        )
        return Post.objects.filter(
            category=self.slug,
            is_published=True,
            pub_date__lte=datetime.now(),
        ).annotate(
            comment_count=Count('comments')
        ).order_by(
            '-pub_date',
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.slug
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        ).order_by(
            'created_at',
        )
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.post_info = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        self.all_post_info = get_object_or_404(Post, pk=self.kwargs["pk"])
        if self.all_post_info.author == self.request.user:
            return Post.objects.all(
            ).annotate(
                comment_count=Count("comments")
            ).order_by(
                "-pub_date"
            ).filter(
                author=self.request.user,
                pk=self.kwargs["pk"],)
        return Post.objects.all(
        ).annotate(
            comment_count=Count("comments")
        ).order_by(
            "-pub_date"
        ).filter(
            is_published=True,
            pk=self.kwargs["pk"],)


class ProfileListView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    ordering = 'pub_date'
    paginate_by = 10
    author = None

    def get_queryset(self):

        self.author = get_object_or_404(
            User,
            username=self.kwargs["username"])

        self.username = get_object_or_404(
            User,
            username=self.kwargs['username']
        )

        return Post.objects.filter(
            author=self.username
        ).annotate(
            comment_count=Count('comments')
        ).order_by(
            '-pub_date'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.author
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    form_class = ProfileForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={
                           'username': self.kwargs['username']})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(PostUpdateDeleteMixinView, UpdateView):
    # В Post и Comment максимально всё убрал в Mixin
    # Функцию dispatch не дает убрать, выводит ошибки.

    def dispatch(self, request, *args, **kwargs):
        one_post = get_object_or_404(Post, pk=self.kwargs['pk'])
        if one_post.author != request.user:
            return redirect('blog:post_detail', pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.kwargs['pk']})


class PostDeleteView(PostUpdateDeleteMixinView, DeleteView):

    def dispatch(self, request, *args, **kwargs):
        one_post = get_object_or_404(Post, pk=self.kwargs['pk'])
        if one_post.author != request.user:
            return redirect('blog:post_detail', pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.object)
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    post_info = None
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        self.post_info = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_info
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            kwargs={'pk': self.kwargs['pk']}
                            )


class CommentUpdateView(CommentUpdateDeleteMixinView, UpdateView):
    form_class = CommentForm


class CommentDeleteView(CommentUpdateDeleteMixinView, DeleteView):
    success_url = reverse_lazy('blog:post_detail')
