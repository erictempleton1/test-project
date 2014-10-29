from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class BlogPost(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    content = models.TextField()
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)

    def save(self):
    	""" Auto saves title as slug, and user as author. """
        self.slug = slugify(self.title)
        self.author = self.user.username
        super(BlogPost, self).save()
		
    def __unicode__(self):
        return self.title

class BlogPostTags(models.Model):
    tag = models.CharField(max_length=100)
    blog_posts = models.ManyToManyField(BlogPost)

    def __unicode__(self):
        return self.tags