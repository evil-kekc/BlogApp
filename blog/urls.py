from django.contrib.sitemaps.views import sitemap
from django.urls import path

from . import views
from .sitemaps import PostSitemap
from .feeds import LatestPostsFeed

app_name = 'blog'

sitemaps = {
    'posts': PostSitemap
}

urlpatterns = [
    path('', views.post_list_view, name='post_list'),
    # path('', views.PostListView.as_view(), name='post_list_view'),
    path('tag/<slug:tag_slug>/', views.post_list_view, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail_view, name='post_detail'),
    path('<int:post_id>/share/', views.post_share_view, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment_view, name='post_comment'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search')

]
