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

    def test_fav_add(self):
    	"""
    	Test that unique posts are saved, and duplicates not added.
    	List len below should be 2.
    	"""
        self.login_example_user()

        # add two unique posts and one duplicate
        test_urls = ['/1/wolf-mustache-fap-umami/favorite/',
                     '/11/etsy-austin/favorite/',
                     '/11/etsy-austin/favorite/']

        for url in test_urls:
           self.driver.get('{0}{1}'.format(
                           self.live_server_url, url))

        # query to verify
        eric = User.objects.get(username='eric')
        me, me_created = UserProfile.objects.get_or_create(user=eric)
        favs = me.favorites.all()

        self.assertEqual(len(favs), 2)

    def test_fav_remove(self):
    	"""
    	Test that posts are added and removed.
    	"""
    	self.login_example_user()

        # add two posts to favorites, and remove one
    	test_urls = ['/1/wolf-mustache-fap-umami/favorite/',
    	             '/11/etsy-austin/favorite/',
    	             '/11/etsy-austin/unfavorite/']

    	for url in test_urls:
    		self.driver.get('{0}{1}'.format(
    			self.live_server_url, url))

        # query to verify
        eric = User.objects.get(username='eric')
        me, me_created = UserProfile.objects.get_or_create(user=eric)
        favs = me.favorites.all()

        self.assertEqual(len(favs), 1)

    def test_load_loggedout(self):
    	"""
    	Test that blog post page loads for un-auth'd user.
    	TypeError is thrown if there is no user object
    	"""
    	response = self.client.get('/11/etsy-austin/')
    	self.assertEqual(response.status_code, 200)

    def test_loggedout_redirect(self):
    	"""
    	Test that un-auth'd user is redirected to login
    	if they try to favorite a post.
    	"""
    	self.driver.get('{0}{1}'.format(
    		self.live_server_url, '/11/etsy-austin/favorite/'))

    	self.assertIn('Password', self.driver.page_source)

    def tearDown(self):
        self.driver.quit()