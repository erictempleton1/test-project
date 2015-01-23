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
    slug = models.SlugField()
    hits = models.PositiveIntegerField(default=0)
    
    def save(self, *args, **kwargs):
    	""" Auto saves title as slug, and user as author. """
        self.slug = slugify(self.title)
        self.author = self.user.username
        super(BlogPost, self).save(*args, **kwargs)
		
    def __unicode__(self):
        return self.title

class BlogPostTags(models.Model):
    tag = models.CharField(max_length=100)
    blog_posts = models.ManyToManyField(BlogPost)

    def __str__(self):
        return self.tag
        
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    favorites = models.ManyToManyField(BlogPost,
        related_name='favorited')
    following = models.ManyToManyField('self',
        related_name='followers',
        symmetrical=False)
    
    def __unicode__(self):
        return self.user.username