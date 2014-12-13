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

# get user object
In [8]: eric = User.objects.get(username='eric')

# add user object to onetoone field
In [9]: me = UserProfile.objects.get_or_create(user=eric)

# get to follow object
In [10]: bill = User.objects.get(username='bill')

# add follow object to onetoone field
In [12]: bill_add = UserProfile.objects.get_or_create(user=bill)

# add follow object 
In [13]: me.following.add(bill)

# get user object
In [10]: eric = User.objects.get(username='eric')

# query UserProfile by object
In [11]: myprofile = get_object_or_404(UserProfile, user = eric)

# return followers
myprofile.following.all()

"""

