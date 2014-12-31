from django.conf import settings
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.test import TestCase, LiveServerTestCase
from django.shortcuts import get_list_or_404, get_object_or_404
from project.models import BlogPost, BlogPostTags, UserProfile
from project.views import (BlogPostCreate, HomePageView, BlogPostDetail, 
	        BlogPostUpdate, BlogPostDelete, ProfileBlog, UserDashboard,
	        BlogTags, AboutPageView, FollowUser, UnfollowUser)

from selenium import webdriver

class FavoritesTest(LiveServerTestCase):

    fixtures = ['user_data.json', 'post_data.json',
	            'tag_data.json', 'user_profile.json']

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.client = Client()

    def test_fav_pageload(self):
        response = self.client.get('/13/sweater-master-cleanse/favorite/')
        # redirects to homepage for right now
        self.assertEqual(response.status_code, 302)

    def tearDown(self):
        self.driver.quit()