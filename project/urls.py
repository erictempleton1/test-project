from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from project.views import BlogPostCreate, HomePageView, BlogPostDetail, BlogPostUpdate, BlogPostDelete, ProfileBlog

urlpatterns = patterns('',
	url(r'^$', HomePageView.as_view(), name='homepage'),
    url(r'create/$', login_required(BlogPostCreate.as_view()), name='create'),
    url(r'(?P<id>\d+)/(?P<slug>[\w-]+)/$', BlogPostDetail.as_view(), name='detail'),
    url(r'(?P<id>\d+)/(?P<slug>[\w-]+)/update/$', login_required(BlogPostUpdate.as_view()), name='update'),
    url(r'(?P<id>\d+)/(?P<slug>[\w-]+)/delete/$', login_required(BlogPostDelete.as_view()), name='delete'),
    url(r'^(?P<author>[\w-]+)/$', ProfileBlog.as_view(), name='profile_detail'),
)