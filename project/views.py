from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView, FormView
from project.models import BlogPost
from django.contrib.auth.models import User
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
