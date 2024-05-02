from django import forms
from django.contrib.auth import get_user_model
from .models import Post, Comment
from django.utils import timezone

User = get_user_model()


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = (
            'author',
        )
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

        def __init__(self, *arg, **kwargs):
            super().__init__(*arg, **kwargs)
            self.fields['pub_date'].initial = timezone.localtime(
                timezone.now()
            ).strftime('%d/%m/%Y, %H:%M:%S')


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = (
            'text',
        )
