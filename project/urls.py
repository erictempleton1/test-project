from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from haystack.views import SearchView
from project.forms import LoginUserForm, CustomForm
from project.views import (BlogPostCreate, HomePageView, BlogPostDetail, 
	        BlogPostUpdate, BlogPostDelete, ProfileBlog, UserDashboard,
	        BlogTags, AboutPageView, FollowUser, UnfollowUser,
            UserFollowers, UserFollowing, FavoritePost, UnfavoritePost,
            FavsView, RegistrationRedirect, UserFeed)

urlpatterns = patterns('',
	url(r'^$', HomePageView.as_view(), name='homepage'),
    url(r'^accounts/register/$', RegistrationRedirect.as_view(), name='reg_redirect'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html', 'authentication_form': LoginUserForm}),
    url(r'about/$', AboutPageView.as_view(), name='about'),
    url(r'create/$', login_required(BlogPostCreate.as_view()), name='create'),
    url(r'(?P<id>\d+)/(?P<slug>[\w-]+)/$', BlogPostDetail.as_view(), name='detail'),
    url(r'(?P<id>\d+)/(?P<slug>[\w-]+)/update/$', login_required(BlogPostUpdate.as_view()), name='update'),
    url(r'(?P<id>\d+)/(?P<slug>[\w-]+)/delete/$', login_required(BlogPostDelete.as_view()), name='delete'),
    url(r'(?P<id>\d+)/(?P<slug>[\w-]+)/favorite/$', login_required(FavoritePost.as_view()), name='favorite'),
    url(r'(?P<id>\d+)/(?P<slug>[\w-]+)/unfavorite/$', login_required(UnfavoritePost.as_view()), name='unfavorite'),
    url(r'tag/(?P<tag>[\w-]+)/$', BlogTags.as_view(), name='tagged_posts'),
    url(r'dashboard/$', login_required(UserDashboard.as_view()), name='user_dashboard'),
    url(r'^(?P<author>[\w-]+)/$', ProfileBlog.as_view(), name='profile_detail'),
    url(r'^(?P<author>[\w-]+)/follow$', login_required(FollowUser.as_view()), name='follow_user'),
    url(r'^(?P<author>[\w-]+)/unfollow$', login_required(UnfollowUser.as_view()), name='unfollow_user'),
    url(r'^(?P<author>[\w-]+)/followers/$', UserFollowers.as_view(), name='user_followers'),
    url(r'^(?P<author>[\w-]+)/following/$', UserFollowing.as_view(), name='user_following'),
    url(r'^(?P<author>[\w-]+)/favorites/$', FavsView.as_view(), name='user_favs'),
    url(r'^home/search/', SearchView(form_class=CustomForm), name='haystack_search'),
    url(r'^home/feed/', login_required(UserFeed.as_view()), name='user_feed'),
)
