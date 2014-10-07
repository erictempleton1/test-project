from django.db import models
from django.template.defaultfilters import slugify

class BlogPost(models.Model):
	title = models.CharField(max_length=100)
	author = models.CharField(max_length=100)
	content = models.TextField()
	submitted = models.CharField(max_length=100)
	slug = models.SlugField()

	def save(self):
		self.slug = slugify(self.title)
		super(BlogPost, self).save()
		
    def __unicode__(self):
        return self.title
	