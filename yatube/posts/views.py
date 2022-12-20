from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from .models import Post, Group, User


def index(request):
    """Главная страница проекта yatube."""

    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)

    posts = Post.objects.all().filter(group=group)[:10]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    """Страница профиля пользователя проекта yatube."""

    user = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=user).all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    posts_count = post_list.count()
    page_obj = paginator.get_page(page_number)
    context = {"author": user,
               "page_obj": page_obj,
               "posts_count": posts_count,
               }
    return render(request, "posts/profile.html", context)


def post_detail(request, username, post_id):
    user_post = get_object_or_404(Post, author__username=username, id=post_id)
    post_count = user_post.author.posts.count()
    context = {
        'author': user_post.author,
        'post_count': post_count,
        'user_post': user_post,
    }
    return render(request, 'posts/post_detail.html', context)
