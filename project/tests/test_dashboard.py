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

class DashboardTest(LiveServerTestCase):

	def setUp(self):
		self.binary = FirefoxBinary(settings.FIREFOX_BIN)
		self.driver = webdriver.Firefox(firefox_binary=self.binary)

	def test_post_delete(self):
		pass

	def tearDown(self):
		self.driver.quit()