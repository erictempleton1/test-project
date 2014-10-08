from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView, FormView
from project.models import BlogPost
from project.forms import BlogForm

class HomePageView(ListView):
	model = BlogPost
	template_name = 'project/index.html'


class BlogPostView(CreateView):
	template_name = 'project/blogpost_form.html'
	form_class = BlogForm
	success_url = '/'
