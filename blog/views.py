import os

from django.contrib.postgres.search import TrigramSimilarity
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from taggit.models import Tag

from .forms import EmailPostForm, CommentForm, SearchForm
from .models import Post


@require_POST
def post_comment_view(request, post_id):
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


def post_list_view(request, tag_slug=None):
    """Displaying posts by page

    :param request: request object
    :param tag_slug: tag slug
    :return: HTTP Response
    """
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    paginator = Paginator(post_list, per_page=3)
    page_number = request.GET.get('page', default=1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'blog/post/list.html',
                  {
                      'posts': posts,
                      'tag': tag
                  })


def post_detail_view(request, year, month, day, post):
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

    comments = post.comments.filter(active=True)
    form = CommentForm()

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    count_of_similar_posts_to_show = 4
    similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
                                 .order_by('-same_tags', '-publish')[:count_of_similar_posts_to_show]

    return render(request,
                  'blog/post/detail.html',
                  {
                      'post': post,
                      'comments': comments,
                      'form': form,
                      'similar_posts': similar_posts
                  })


def post_share_view(request, post_id):
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


def post_search(request):
    """Search for posts by match in the title and body of the Post model

    :param request: request object
    :return: HTTP Response
    """
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
                similarity=TrigramSimilarity('title', query),
            ).filter(similarity__gt=0.1).order_by('-similarity')

    return render(request,
                  'blog/post/search.html',
                  {
                      'form': form,
                      'query': query,
                      'results': results
                  })
