from django.contrib import admin
from project.models import BlogPost, UserProfile


# Register your models here.
admin.site.register(BlogPost)
admin.site.register(UserProfile)