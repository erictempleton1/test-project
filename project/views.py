from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView, FormView
from project.models import BlogPost
from project.forms import BlogForm


class BlogPostView(FormView):
	template_name = 'project/blogpost_form.html'
	form_class = BlogForm
	success_url = '/'
