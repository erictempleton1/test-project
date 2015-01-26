from django.contrib import admin
from project.models import BlogPost, BlogPostTags, UserProfile


# Register your models here.
models = [BlogPost, BlogPostTags, UserProfile]
admin.site.register(models)