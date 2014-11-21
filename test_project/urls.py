from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'test_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls'))
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('project.urls', namespace="project")),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^summernote/', include('django_summernote.urls')),
)