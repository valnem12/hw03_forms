from django.forms import ModelForm
from django import forms

from posts.models import Post, Group


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
