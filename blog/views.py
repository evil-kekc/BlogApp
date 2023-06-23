from django.shortcuts import render, get_object_or_404

from .models import Post


def post_list(request):
    """List of posts

    :param request: request object
    :return: HTTP Response
    """
    posts = Post.objects.all()
    return render(request,
                  'blog/post/list.html',
                  {
                      'posts': posts
                  })


def post_detail(request, id):
    """Post details

    :param request: request object
    :param id: post id
    :return: HTTP Response
    """
    post = get_object_or_404(Post,
                             id=id,
                             status=Post.Status.PUBLISHED)

    return render(request,
                  'blog/post/detail.html',
                  {
                      'post': post
                  })
