from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView, FormView
from project.models import BlogPost
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from project.forms import BlogForm

class HomePageView(ListView):
	""" Lists all blog posts for every user. """
	model = BlogPost
	template_name = 'project/index.html'

class BlogPostDetail(DetailView):
	""" Single blog post content viewable by all users. """
	model = BlogPost
	template_name = 'project/blogpost_list.html'

class BlogPostCreate(CreateView):
	""" Requires login, and saves to logged in user. """
	template_name = 'project/blogpost_form.html'
	form_class = BlogForm
	success_url = '/'

	def form_valid(self, form):
		""" Attributes blog post to "user" foreignkey from models. """
		form.instance.user = self.request.user
		return super(BlogPostCreate, self).form_valid(form)

	def form_invalid(self, form):
		return self.render_to_response(self.get_context_data(form=form))

class BlogPostUpdate(UpdateView):
	""" Requires login, and only post author can edit. """
	model = BlogPost
	form_class = BlogForm

	def get_queryset(self):
		""" 
		Overrides default queryset to only allow post creator
		to update, and raises 404 error otherwise.
		"""
		user_set = super(BlogPostUpdate, self).get_queryset()
		return user_set.filter(user=self.request.user)

	def get_success_url(self):
		return reverse('project:blog_content', kwargs={
			'id': self.object.id,
			'slug': self.object.slug,
			})

class BlogPostDelete(DeleteView):
	""" Requires login, and only post author can delete """
	model = BlogPost
	success_url = '/'

	def get_queryset(self):
		user_set = super(BlogPostDelete, self).get_queryset()
		return user_set.filter(user=self.request.user)

class UserBlogPosts(ListView):
	""" Lists posts by specific user """
	model = BlogPost
	template_name = 'project/user_page.html'

	def get_queryset(self):
		""" Queries based on url param """
		self.author = self.kwargs['author']
		user_posts = super(UserBlogPosts, self).get_queryset()
		return user_posts.filter(author=self.author)
