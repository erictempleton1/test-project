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

        test_urls = ['/1/wolf-mustache-fap-umami/favorite/',
                     '/11/etsy-austin/favorite/',
                     '/11/etsy-austin/favorite/']

        for url in test_urls:
           self.driver.get('{0}{1}'.format(
                           self.live_server_url, url))          

        eric = User.objects.get(username='eric')
        me, me_created = UserProfile.objects.get_or_create(user=eric)
        favs = me.favorites.all()

        print favs
        print len(favs)
        self.assertEqual(len(favs), 2)

    def test_fav_remove(self):
    	response = self.client.get('/1/wolf-mustache-fap-umami/unfavorite/')
    	self.assertEqual(response.status_code, 302)

    def tearDown(self):
        self.driver.quit()