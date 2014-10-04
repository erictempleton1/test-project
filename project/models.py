from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Post(models.Model):
	user = models.ForeignKey(User)
	title = models.CharField(max_length=100)
	author = models.CharField(max_length=100)
	content = models.TextField()
	slug = models.SlugField()

	def save(self):
		self.slug = slugify(self.title)
		super(Post, self).save()
	