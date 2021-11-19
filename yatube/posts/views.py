from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import Post, Group
from .forms import PostForm
from yatube.settings import POSTS_PER_PAGE


User = get_user_model()


def _pagination(request, selector, count=POSTS_PER_PAGE):
    paginator = Paginator(selector, count)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    """Main page - dispalying the latest ten posts."""

    template = 'posts/index.html'
    posts = Post.objects.all()
    page_obj = _pagination(request, posts)
    context = {
        'page_obj': page_obj
    }
    return render(request, template, context)


def group_posts(request, slug):
    """Filters by group and displays posts by ten per page."""

    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts_by_group = group.posts.all()
    context = {
        'group': group,
        'page_obj': _pagination(request, posts_by_group),
    }
    return render(request, template, context)


def profile(request, username):
    """Filters by author and displays posts by ten per page."""

    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    posts_by_author = author.posts.all()
    context = {
        'author': author,
        'page_obj': _pagination(request, posts_by_author),
    }
    return render(request, template, context)


def post_detail(request, post_id):
    """Filters by author and displays posts by ten per page."""

    template = 'posts/post_detail.html'
    post_by_text_id = get_object_or_404(Post, pk=post_id)
    context = {
        'post_by_text_id': post_by_text_id,
        'post_count': post_by_text_id.author.posts.count()
    }
    return render(request, template, context)


@login_required(redirect_field_name=None)
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=request.user)
    return render(request, 'posts/post_create.html', {'form': form})


@login_required(redirect_field_name=None)
def post_edit(request, post_id):

    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST or None, instance=post)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)
    return render(request,
                  'posts/post_create.html',
                  {'form': form,
                   'is_edit': True,
                   'post_id': post_id}
                  )
