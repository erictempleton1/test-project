from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from project.models import Post
from project.forms import BlogForm
from django.core.urlresolvers import reverse

class PostListing(ListView):
	model = Post

class PostCreate(CreateView):
	model = Post
	success_url = '/'

class PostDetail(DetailView):
	model = Post

class PostUpdate(UpdateView):
	model = Post
	success_url = '/'

class PostDelete(DeleteView):
    model = Post
    success_url = '/'
