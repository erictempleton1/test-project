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
    user = models.OneToOneField(User)
    following = models.ManyToManyField('self', related_name='followers', symmetrical=False)
    
    def __unicode__(self):
        return self.user.username
        

# work on hit counter for detail view
# for reference - https://github.com/renyi/django-pageviews/blob/master/pageviews/middleware.py
  
""" 
Query notes for later

n [1]: from django.shortcuts import get_object_or_404

In [2]: from django.contrib.auth.models import User

In [3]: from project.models import BlogPost, BlogPostTags, UserProfile

In [4]: eric = User.objects.get(username='eric')

In [5]: me, me_created = UserProfile.objects.get_or_create(user=eric)

In [6]: me
Out[6]: <UserProfile: eric>

In [7]: bill = User.objects.get(username='bill')

In [8]: add_bill, follow_created = UserProfile.objects.get_or_create(user=bill)

In [9]: add_bill
Out[9]: <UserProfile: bill>

In [10]: me.following.add(add_bill)

In [11]: myprofile = get_object_or_404(UserProfile, user=eric)

In [12]: myprofile.following.all()
Out[12]: [<UserProfile: bill>]

"""

