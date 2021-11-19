from django.forms import ModelForm
from posts.models import Post, Group


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ('text', 'group')
        labels = {
            'text': ('Текст поста'),
            'group': ('Group')
        }
        help_texts = {
            'text': ('Текст нового поста.'),
            'group': ('Группа, к которой будет относиться пост')
        }
