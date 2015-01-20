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

class RegRedirectTest(LiveServerTestCase):

	fixtures = ['user_data.json', 'post_data.json',
	            'tag_data.json', 'user_profile.json']

	def setUp(self):
		self.binary = FirefoxBinary(settings.FIREFOX_BIN)
		self.driver = webdriver.Firefox(firefox_binary=self.binary)
		self.clien = Client()

	def submit_reg_form(self):
		driver = self.driver
		self.driver.get(
			'{0}{1}'.format(self.live_server_url, '/accounts/register'))

		self.driver.find_element_by_id('id_username').send_keys('eric4')
		self.driver.find_element_by_id('id_email').send_keys('eric4@eric4.com')
		self.driver.find_element_by_id('id_password1').send_keys('eric')
		self.driver.find_element_by_id('id_password2').send_keys('eric')

		self.driver.find_element_by_xpath(
			'/html/body/div[2]/div/div/form/input[2]').click()

	def test_reg_redirect(self):
		driver = self.driver
		self.submit_reg_form()
		
		self.assertIn('eric4', self.driver.page_source)

	def tearDown(self):
		self.driver.quit()
