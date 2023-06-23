from django.shortcuts import render, get_object_or_404

from .models import Post


def post_list(request):
    """List of posts

    :param request: request object
    :return: HTTP Response
    """
    posts = Post.published.all()
    return render(request,
                  'blog/post/list.html',
                  {
                      'posts': posts
                  })


def post_detail(request, year, month, day, post):
    """Post details

    :param post: post slug
    :param day: post publish day
    :param month: post publish month
    :param year: post publish year
    :param request: request object
    :return: HTTP Response
    """
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    return render(request,
                  'blog/post/detail.html',
                  {
                      'post': post
                  })
