import random
from django.contrib.auth.models import User
from project.models import BlogPost, BlogPostTags, UserProfile

from faker import Factory
fake = Factory.create()

def create_users(num):
    """
    Creates num amount of random users.
    Catches error for existing usernames.
    """
    users = []
    for person in range(1, num):
        user = User(
        	username=fake.first_name(),
        	email=fake.safe_email(),
        	password='password'
        	)
        users.append(user)
    try:
        User.objects.bulk_create(users)
    except IntegrityError:
    	print 'One of the usernames already exists'

    return User.objects.all().order_by('-id')[:num-1]

def single_user_posts(username, num):
	"""
	Creates num amount of posts for given user.
	Faker adds a period on sentences, so a slice
	is used to drop the period for title.
	Not the most effecient method for saving posts.
	"""
	current_user = User.objects.get(username=username)
	for post in range(1, num):
		current_user.blogpost_set.create(
			title=fake.sentence(
				nb_words=5,
				variable_nb_words=True)[:-1],
			content=fake.paragraph(
				nb_sentences=10,
				variable_nb_sentences=True)
			)
		current_user.save()
	return BlogPost.objects.all().order_by('-id')[:num-1]

def random_user_posts(num):
	all_users = User.objects.all()
	usernames = [str(user.username) for user in all_users]
	
	for post in range(1,num):
		current_user = User.objects.get(username=random.choice(usernames))
		current_user.blogpost_set.create(
			title=fake.sentence(
				nb_words=5,
				variable_nb_words=True)[:-1],
			content=fake.paragraph(
				nb_sentences=10,
				variable_nb_sentences=True),
			)
		current_user.save()
	return BlogPost.objects.all().order_by('-id')[:num-1]


