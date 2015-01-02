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

    def login_example_user(self):
    	""" Log in when needed """
    	driver = self.driver
    	self.driver.get(
    		'{0}{1}'.format(self.live_server_url, '/accounts/login/'))

    	self.driver.find_element_by_id('id_username').send_keys(
    		settings.EXAMPLE_USERNAME)
    	self.driver.find_element_by_id('id_password').send_keys(
    		settings.EXAMPLE_PASSWORD)

    	self.driver.find_element_by_xpath(
    		'/html/body/div[2]/div/div/form/input[2]').click()

    def test_fav_pageload(self):
        response = self.client.get('/13/sweater-master-cleanse/favorite/')
        self.login_example_user()
        
        eric = User.objects.get(username='eric')
        me, me_created = UserProfile.objects.get_or_create(user=eric)
        post_fav = BlogPost.objects.get(id=13)
        fav_exists = me.favorites.get(favorites=post_fav)

        self.assertTrue(fav_exists)
        self.assertEqual(response.status_code, 302)

    def tearDown(self):
        self.driver.quit()