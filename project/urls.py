from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from project.views import BlogPostView, HomePageView

urlpatterns = patterns('',
	url(r'^$', HomePageView.as_view(), name='homepage'),
    url(r'create/$', login_required(BlogPostView.as_view()), name='listing'),

)