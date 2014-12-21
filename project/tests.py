from django.test import TestCase, LiveServerTestCase
from django.test import TestCase, Client
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

    def test_follow(self):
    	"""
    	Tests follow button on user profile page.
    	User directed to login page if follow button is clicked,
    	and they are not already logged in.
    	"""
    	driver = self.driver
        self.driver.get(
            '{0}{1}'.format(self.live_server_url, '/eric/')
            )

        # click follow button
        self.driver.find_element_by_xpath(
        	'/html/body/div[2]/div/div/ul/h4/a/button').click()

        # check that un-authd user is taken to login page on follow click
        self.assertIn('Username', self.driver.page_source)

    def test_follow_loggedin(self):
    	driver = self.driver
    	self.driver.get(
    		'{0}{1}'.format(self.live_server_url, '/accounts/login/')
    		)
    	
    	# log in as example user
    	self.driver.find_element_by_id('id_username').send_keys('eric')
    	self.driver.find_element_by_id('id_password').send_keys('eric')
    	self.driver.find_element_by_xpath(
    		'/html/body/div[2]/div/div/form/input[2]').click()

        self.assertIn('Logout', self.driver.page_source)

    def tearDown(self):
    	self.driver.quit()
