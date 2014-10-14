from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from project.views import BlogPostCreate, HomePageView, BlogPostList, BlogPostUpdate

urlpatterns = patterns('',
	url(r'^$', HomePageView.as_view(), name='homepage'),
    url(r'create/$', login_required(BlogPostCreate.as_view()), name='create'),
    url(r'(\d+)/(?P<slug>[\w-]+)/$', BlogPostList.as_view(), name='listing'),
    url(r'(\d+)/(?P<slug>[\w-]+)/update/$', login_required(BlogPostUpdate.as_view()), name='update'),
)