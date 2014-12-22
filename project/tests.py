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
    	Test to be sure follow button is hidden if user views own profile.
    	"""
    	driver = self.driver
    	self.login_example_user()

        self.driver.get(
        	'{0}{1}'.format(self.live_server_url, '/eric/')
        	)

        # 'pull-right' only exists when follow/unfollow button is shown
        self.assertNotIn('pull-right', self.driver.page_source)

    def follow_exists(self):
    	""" 
    	Query to see if follow exists between example user 
    	and another user.
    	"""
    	user_follow = get_object_or_404(User, username='bill')
        eric = get_object_or_404(User, username='eric')
        me, me_created = UserProfile.objects.get_or_create(user=eric)
        follow_exists = me.following.filter(user=user_follow).exists()
        return follow_exists


    def test_follow_add(self):
        """ Test click to be sure that 'Follow' adds user """
    	driver = self.driver
    	self.login_example_user()

        # visit other user's profile page
    	self.driver.get(
    		'{0}{1}'.format(self.live_server_url, '/bill/')
    		)

        # once follow is clicked, exists() is True
        self.driver.find_element_by_xpath(
        	'/html/body/div[2]/div/div/ul/h4/a/button').click()

        self.assertEqual(self.follow_exists(), True)

    def test_follow_remove(self):
    	driver = self.driver
    	self.login_example_user()

    	self.driver.get(
    		'{0}{1}'.format(self.live_server_url, '/bill/')
    		)

        # click once to follow
    	self.driver.find_element_by_xpath(
    		'/html/body/div[2]/div/div/ul/h4/a/button').click()

    	# click again to unfollow
    	self.driver.find_element_by_xpath(
    		'/html/body/div[2]/div/div/ul/h4/a/button').click()

    	self.assertEqual(self.follow_exists(), False)

    def tearDown(self):
    	self.driver.quit()

