from django.shortcuts import render
from django.views.generic import ListView, CreateView
from project.models import Post

class PostListing(ListView):
	model = Post

class PostCreate(CreateView):
	model = Post
	success_url = '/'