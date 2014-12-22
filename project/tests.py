from django.test import TestCase, LiveServerTestCase
from django.test import TestCase, Client
from django.conf import settings
from project.models import BlogPost, BlogPostTags, UserProfile
from project.views import (BlogPostCreate, HomePageView, BlogPostDetail, 
	        BlogPostUpdate, BlogPostDelete, ProfileBlog, UserDashboard,
	        BlogTags, AboutPageView, FollowUser, UnfollowUser)

from selenium import webdriver


class ProfilePageTest(LiveServerTestCase):

    fixtures = ['user_data.json', 'post_data.json',
                'tag_data.json', 'user_profile.json']
   
    def setUp(self):
    	self.driver = webdriver.Firefox()
        self.client = Client()

    def login_example_user(self):
    	""" Log in when needed """
    	driver = self.driver
    	self.driver.get(
    		'{0}{1}'.format(self.live_server_url, '/accounts/login/')
    		)

    	# log in as example user
    	self.driver.find_element_by_id('id_username').send_keys(
    		settings.EXAMPLE_USERNAME)
    	self.driver.find_element_by_id('id_password').send_keys(
    		settings.EXAMPLE_PASSWORD)

    	# click login button
    	self.driver.find_element_by_xpath(
    		'/html/body/div[2]/div/div/form/input[2]').click()

    def test_follow(self):
    	"""
    	Test that user is taken to login page if they
    	click follow and they are not logged in.
    	"""
    	driver = self.driver

        # view a user's page when not logged in
        self.driver.get(
            '{0}{1}'.format(self.live_server_url, '/bill/')
            )

        # click follow button
        self.driver.find_element_by_xpath(
        	'/html/body/div[2]/div/div/ul/h4/a/button').click()

        # check that un-authd user is taken to login page on follow click
        self.assertIn('Username', self.driver.page_source)

    def test_follow_self(self):
    	"""
    	Test to be sure follow button is hidden for if user views own profile.
    	"""
    	driver = self.driver
    	self.login_example_user()

        self.driver.get(
        	'{0}{1}'.format(self.live_server_url, '/eric/')
        	)

        # 'pull-right' only exists when follow/unfollow button is shown
        self.assertNotIn('pull-right', self.driver.page_source)

    def tearDown(self):
    	self.driver.quit()
