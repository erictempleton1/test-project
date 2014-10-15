from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView, FormView
from project.models import BlogPost
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from project.forms import BlogForm

class HomePageView(ListView):
	model = BlogPost
	template_name = 'project/index.html'

class BlogPostCreate(CreateView):
	template_name = 'project/blogpost_form.html'
	form_class = BlogForm
	success_url = '/'

	def form_valid(self, form):
		# saves blog post to "user" foreignkey from models.py
		form.instance.user = self.request.user
		return super(BlogPostCreate, self).form_valid(form)

	def form_invalid(self, form):
		return self.render_to_response(self.get_context_data(form=form))
		
class BlogPostList(DetailView):
	model = BlogPost
	template_name = 'project/blogpost_list.html'

class BlogPostUpdate(UpdateView):
	model = BlogPost
	form_class = BlogForm

	def get_queryset(self):
		# overrides default queryset to only allow post creator
		# raises 404 if user is not creator
		user_set = super(BlogPostUpdate, self).get_queryset()
		return user_set.filter(user=self.request.user)

	def get_success_url(self):
		return reverse('project:blog_content', kwargs={
			'id': self.object.id,
			'slug': self.object.slug,
			})
