from django.shortcuts import render, get_object_or_404

from .models import Post


def post_list(request):
    """

    :param request:
    :return:
    """
    posts = Post.objects.all()
    return render(request,
                  'blog/post/list.html',
                  {
                      'posts': posts
                  })


def post_detail(request, id_):
    """Детальная информация о посте

    :param request:
    :param id_:
    :return:
    """
    post = get_object_or_404(Post,
                             id=id,
                             status=Post.Status.PUBLISHED)

    return render(request,
                  'blog/post/detail.html',
                  {
                      'post': post
                  })
