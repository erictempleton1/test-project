from django.conf.urls import patterns, url
from project.views import PostListing, PostCreate, PostDetail, PostUpdate

urlpatterns = patterns('', url(r'^$', PostListing.as_view(), name='listing'),
	                       url(r'^create/$', PostCreate.as_view(), name='create'),
	                       url(r'^(?P<pk>\d+)/$', PostDetail.as_view(), name='detail'),
	                       url(r'^(?P<pk>\d+)/update/$', PostUpdate.as_view(), name='update'),
)