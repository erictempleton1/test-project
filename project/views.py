from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from project.models import BlogPost, UserProfile
from django.contrib.auth.models import User
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
	form_class = BlogForm
	template_name = 'project/blogpost_form.html'
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
		return reverse('project:detail', kwargs={
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

class ProfileBlog(ListView):
	""" Lists all posts by specific user """
	model = BlogPost
	template_name = 'project/profile_blog.html'

	def get_queryset(self):
		""" Queries based on url param """
		self.author = self.kwargs['author']
		profile_posts = super(ProfileBlog, self).get_queryset()
		return profile_posts.filter(author=self.author)

	def get_context_data(self, **kwargs):
		context = super(ProfileBlog, self).get_context_data(**kwargs)
		context['author'] = self.kwargs['author']
		return context

class UserDashboard(ListView):
	""" Dashboard where a user can view/edit/delete their posts """
	model = BlogPost
	template_name = 'project/user_profile.html'

	def get_queryset(self):
		pass

	def get_context_data(self, **kwargs):
		context = super(UserDashboard, self).get_context_data(**kwargs)
		context['user'] = self.kwargs['user']
		return context