from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    """Returns count of posts

    :return: count of posts
    """
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    """Returns similar latest posts

    :param count: count of posts
    :return: latest posts
    """
    latest_posts = Post.published.order_by('-publish')[:count]
    return {
        'latest_posts': latest_posts
    }


@register.simple_tag
def get_most_commented_posts(count=5):
    """Returns most commented posts

    :param count: count of posts
    :return: most commented posts
    """
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    """Converts markdown to HTML format

    :param text: text
    :return: mark safe object
    """
    return mark_safe(markdown.markdown(text))
