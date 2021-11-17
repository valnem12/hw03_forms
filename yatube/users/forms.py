from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django import forms

from posts.models import Post, Group


User = get_user_model()


class CreationForm(UserCreationForm):

    first_name = forms.CharField(
        max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(
        max_length=30, required=False, help_text='Optional')
    username = forms.CharField(
        max_length=30, required=True, help_text='Username is required')
    email = forms.EmailField(
        required=True, max_length=254,
        help_text='Enter a valid email address')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class PostForm(ModelForm):

    text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 12, 'cols': 66}),
        label='Текст поста',
        required=True,
        help_text='Текст нового поста')

    group = (
        forms.ModelChoiceField(
            queryset=Group.objects.filter(title__isnull=False),
            required=False,
            help_text='Группа, к которой будет относиться пост'
        )
    )

    class Meta:
        model = Post
        fields = ('text', 'group')
