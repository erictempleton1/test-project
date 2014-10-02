from django.conf.urls import patterns, url
from project.views import PostListing, PostCreate, PostDetail

urlpatterns = patterns('', url(r'^$', PostListing.as_view(), name='listing'),
	                       url(r'^create/$', PostCreate.as_view(), name='create'),
	                       url(r'^(?P\d+)/$', PostDetail.as_view(), name='detail'),
)