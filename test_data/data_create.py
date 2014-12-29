from django.contrib.auth.models import User
from project.models import BlogPost, BlogPostTags, UserProfile

from faker import Factory
fake = Factory.create()

def create_users(num):
    users = []
    for person in range(1,num):
        user = User(
        	username=fake.user_name(),
        	email=fake.safe_email(),
        	password='password')
        users.append(user)
    User.objects.bulk_create(users)
    return User.objects.all().order_by('-id')[:num]

