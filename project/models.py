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
        return self.tag
        
class UserProfile(models.Model):
    user = models.ForeignKey(User)
    following = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)
    
    def __unicode__(self):
        return str(self.following)
        

# work on hit counter for detail view
# for reference - https://github.com/renyi/django-pageviews/blob/master/pageviews/middleware.py
  
""" 
Query notes for later

In [5]: user_to_follow = User.objects.get(username='erictempleton')

In [6]: f = UserProfile(user=eric)

In [7]: f.save()

In [8]: f.following.add(user_to_follow.id)

"""

