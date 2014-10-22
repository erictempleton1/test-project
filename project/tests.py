from django.test import TestCase
from django.test import TestCase, Client
from project.models import BlogPost, UserProfile
from project.views import BlogPostCreate, HomePageView, BlogPostDetail, BlogPostUpdate, BlogPostDelete, ProfileBlog, UserProfile

class ViewTest(TestCase):

	def SetUp(self):
		self.client = Client()

	def test_profile_page(self):
		response = self.client.get('eric/dashboard/')
		self.assertEquals(response.status_code, 200)
