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
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

class CreatePostTest(LiveServerTestCase):

    fixtures = ['user_data.json', 'post_data.json',
	            'tag_data.json', 'user_profile.json']

    def setUp(self):
        self.binary = FirefoxBinary(settings.FIREFOX_BIN)
        self.driver = webdriver.Firefox(firefox_binary=self.binary)
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
    		'/html/body/div[2]/div/div/div/div/form/button').click()

        # go to create post page
    	self.driver.get(
    		'{0}{1}'.format(self.live_server_url, '/create/'))

    def test_page_load(self):
    	"""
    	Basic test to ensure create page loads for auth'd user
    	"""
    	driver = self.driver
    	self.login_example_user()
    	self.assertIn('Title', self.driver.page_source)

    def test_body_error(self):
    	"""
    	Test that error shows up for no body text on submit.
    	Not able to find body xpath for some reason,
    	but manual test shows that error displays for missing
    	title as well.
    	"""
    	driver = self.driver
    	self.login_example_user()

    	self.driver.find_element_by_xpath(
    		'//*[@id="id_title"]').send_keys('Title')

    	self.driver.find_element_by_xpath(
    		'/html/body/div[2]/div/form/button').click()
    	
    	self.assertIn('required', self.driver.page_source)

    def tearDown(self):
    	self.driver.quit()