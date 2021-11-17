from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, Page
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages

from .models import Post, Group
from users.forms import PostForm


User = get_user_model()


def _pagination(request, selector, count):
    paginator = Paginator(selector, count)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


# @login_required(redirect_field_name=None)
def index(request):
    """Main page - dispalying the latest ten posts."""

    template = 'posts/index.html'
    posts = Post.objects.all()
    page_obj = _pagination(request, posts, 10) 
    context = {
        'posts': posts,
        'page_obj': page_obj
    }
    return render(request, template, context)


#@login_required(redirect_field_name=None)
def group_posts(request, slug):
    """Filters by group and displays posts by ten per page."""

    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts_by_group = (group
                      .posts
                      .all())                
    context = {
        'group': group,
        'posts_by_group': posts_by_group,
        'page_obj': _pagination(request, posts_by_group, 10),
    }
    return render(request, template, context)


#@login_required(redirect_field_name=None)
def profile(request, username):
    """Filters by author and displays posts by ten per page."""

    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    posts_by_author = (author
                       .posts
                       .filter(author=author)
                       )
    context = {
        'author': author,
        'page_obj': _pagination(request, posts_by_author, 10),
    }
    return render(request, template, context)


#@login_required(redirect_field_name=None)
def post_detail(request, post_id):
    """Filters by author and displays posts by ten per page."""

    template = 'posts/post_detail.html'
    text_by_id = get_object_or_404(Post, pk=post_id)
    context = {
        'text_by_id': text_by_id,
        'post_count': text_by_id.author.posts.count
    }
    return render(request, template, context)


@login_required(redirect_field_name=None)
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        form.cleaned_data['text']
        #form.cleaned_data['group']
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=post.author)
    return render(request, 'posts/post_create.html', {'form': form})


@login_required(redirect_field_name=None)
def post_edit(request, post_id):

    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST or None, initial={'text': post.text})
    is_edit = True
    if post.author != request.user:
        messages.warning(request, 'You can\'t modify others posts')
        return redirect('posts:post_detail', post_id)
    if form.is_valid():
        post.text = form['text'].value()
        post.save()
        return redirect('posts:post_detail', post_id)
    return render(request,
                  'posts/post_create.html',
                  {'form': form,
                   'is_edit': is_edit,
                   'post_id': post_id}
                  )
