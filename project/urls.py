from django.conf.urls import patterns, url
from project.views import BlogPostView

urlpatterns = patterns('', url(r'^$', BlogPostView.as_view(), name='listing'),

)