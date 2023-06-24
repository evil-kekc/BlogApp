import os

from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .forms import EmailPostForm, CommentForm
from .models import Post, Comment
from django.views.decorators.http import require_POST


@require_POST
def post_comment(request, post_id):
    """Saving a comment on a post

    :param request: request object
    :param post_id: post id
    :return: HTTP response
    """
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)

    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request, 'blog/post/comment.html',
                  {
                      'post': post,
                      'form': form,
                      'comment': comment
                  })


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


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


def post_share(request, post_id):
    """Sending a post by email

    :param request: request object
    :param post_id: post id
    :return: HTTP Response
    """
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)

    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = f"{cd['name']} recommended you read " \
                      f"{post.title}"
            message = f'Read {post.title} at {post_url}\n\n' \
                      f"{cd['name']}\'s comments: {cd['comments']}"

            send_mail(subject, message, os.getenv('ADMIN_GMAIL'), [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {
        'post': post,
        'form': form,
        'sent': sent
    })
