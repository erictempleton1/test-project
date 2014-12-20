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

    def test_profile_page(self):
    	driver = self.driver
        self.driver.get(
            '{0}{1}'.format(self.live_server_url, '/eric/')
        )
        elem = driver.find_element_by_xpath('/html/body/div[2]/div/div/ul/h4/a')
        self.assertIn('Follow', self.driver.page_source)

    def tearDown(self):
    	self.driver.quit()
