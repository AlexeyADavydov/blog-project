from django.urls import path
from blog.views import (IndexListView,
                        ProfileListView,
                        CategoryListView,
                        ProfileUpdateView,
                        PostDetailView,
                        PostCreateView,
                        PostUpdateView,
                        PostDeleteView,
                        CommentCreateView,
                        CommentUpdateView,
                        CommentDeleteView,
                        )

from django.conf.urls.static import static
from django.conf import settings

app_name = 'blog'

urlpatterns = [
    path('',
         IndexListView.as_view(),
         name='index',),

    path('posts/<int:pk>/',
         PostDetailView.as_view(),
         name='post_detail',),

    path('<slug:slug>/',
         CategoryListView.as_view(),
         name='category_posts',),

    path(
        'profile/<slug:username>/',
        ProfileListView.as_view(),
        name='profile',
    ),

    path(
        'profile/<slug:username>/edit/',
        ProfileUpdateView.as_view(),
        name='edit_profile',
    ),

    path('posts/create/',
         PostCreateView.as_view(),
         name='create_post'),

    path(
        'posts/<int:pk>/edit/',
        PostUpdateView.as_view(),
        name='edit_post'
    ),

    path(
        'posts/<int:pk>/delete/',
        PostDeleteView.as_view(),
        name='delete_post'
    ),

    path(
        'posts/<int:pk>/comment/',
        CommentCreateView.as_view(),
        name='add_comment'
    ),

    path(
        'posts/<int:pk>/comment/<int:comment_id>/edit_comment/',
        CommentUpdateView.as_view(),
        name='edit_comment'
    ),

    path(
        'posts/<int:pk>/comment/<int:comment_id>/delete_comment/',
        CommentDeleteView.as_view(),
        name='delete_comment'
    ),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
