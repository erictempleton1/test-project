from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, FormView
from project.models import Post
from django.core.urlresolvers import reverse

class PostListing(ListView):
	model = Post

class PostCreate(CreateView):
	model = Post
	fields = ['title', 'author', 'content']
	success_url = '/'

class PostDetail(DetailView):
	model = Post

class PostUpdate(UpdateView):
	model = Post
	field = ['title', 'author', 'content']
	success_url = '/'

class PostDelete(DeleteView):
    model = Post
    success_url = '/'

