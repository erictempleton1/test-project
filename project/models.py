from django.db import models
from django.template.defaultfilters import slugify

class Post(models.Model):
	title = models.CharField(max_length=100)
	author = models.CharField(max_length=100)
	content = models.TextField()
	slug = models.SlugField()

	def save(self):
		self.slug = slugify(self.title)
		super(Post, self).save()
	