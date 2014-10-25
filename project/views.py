from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from project.models import BlogPost, BlogPostTags
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

    def get_context_data(self, **kwargs):
    	""" Query to return blog tags based on blog post id from url param """
        context = super(BlogPostDetail, self).get_context_data(**kwargs)
        blog_id = self.kwargs['id']
        blog_tags = BlogPost.objects.get(pk=blog_id)
        context['tags'] = blog_tags.blogposttags_set.all()
        return context

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
        """ Queries posts by auth'd user """
        user_posts = super(UserDashboard, self).get_queryset()
        return user_posts.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        """ Uses auth'd user as context var to template """
        context = super(UserDashboard, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class BlogTags(ListView):
	""" Lists blog posts with a certain tag """
	model = BlogPostTags
	template_name = 'project/tag_blogs.html'

	def get_query_set(self):
		self.tag = self.kwargs['tags']
		blog_tag = super(BlogTags, self).get_queryset()
		return BlogPost.objects.filter(blogposttags__tags=self.tag)

	def get_context_data(self, **kwargs):
		context = super(BlogTags, self).get_context_data(**kwargs)
		context['tag'] = self.kwargs['tags']
		return context