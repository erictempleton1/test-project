from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from project.models import Post
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

	def get_success_url(self):
		return reverse('project:detail', kwargs={'pk': self.object.pk,})

