from django.conf.urls import patterns, url
from project.views import PostListing, PostCreate, PostDetail, PostUpdate, PostDelete

urlpatterns = patterns('', url(r'^$', PostListing.as_view(), name='listing'),
	                       url(r'^create/$', PostCreate.as_view(), name='create'),
	                       url(r'^(?P<slug>[-\w]+)/$', PostDetail.as_view(), name='detail'),
	                       url(r'^(?P<slug>[-\w]+)/update/$', PostUpdate.as_view(), name='update'),
	                       url(r'^(?P<pk>\d+)/delete/$', PostDelete.as_view(), name='delete'),
)