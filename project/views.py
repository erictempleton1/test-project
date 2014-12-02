from django.views.generic import (ListView, CreateView, DetailView,
                    UpdateView, DeleteView, TemplateView, FormView)
from django.contrib import messages
from django.views.generic.edit import FormMixin
from project.models import BlogPost, BlogPostTags, UserProfile
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from project.forms import BlogForm, BlogPostTagsForm
from collections import Counter

class HomePageView(ListView):
    """ Lists all blog posts for every user. """
    model = BlogPost
    template_name = 'project/index.html'

    def get_context_data(self, **kwargs):
        """ Returns all posts sorted by most recent """
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['all_posts'] = BlogPost.objects.all().order_by('-added')
        context['tag_count'] = self.tag_count(BlogPostTags.objects.all())
        return context

    def tag_count(self, tags):
    	""" Creates tuple of tags by most popular, and provides count """
        clean_tags = [str(tag) for tag in tags]
        c = Counter(clean_tags)
        return c.most_common()

class AboutPageView(TemplateView):
	model = BlogPost
	template_name = 'project/about.html'

class BlogPostDetail(SuccessMessageMixin, FormView):
    """ Single blog post content viewable by all users. """
    model = BlogPost
    form_class = BlogPostTagsForm
    template_name = 'project/blogpost_list.html'
    success_message = 'Tag added!'

    def get_context_data(self, **kwargs):
        """ Gets post, and tags for post by id """
        context = super(BlogPostDetail, self).get_context_data(**kwargs)
        self.id = self.kwargs['id']
        context['blog_post'] = BlogPost.objects.get(id=self.id)
        context['tags'] = BlogPost.objects.get(id=self.id).blogposttags_set.all()
        context['current_user'] = str(self.request.user)
        return context

    def form_valid(self, form):
    	""" Uses url param id to query current post """
        self.blog_id = self.kwargs['id']
        self.blog_tag = form.cleaned_data['tag'].lower()
        tag_exists = BlogPostTags.objects.filter(
        	blog_posts__id=self.blog_id).filter(
        	tag=self.blog_tag).exists()

        if not tag_exists:
	        """ 
	        Checks if tag exists, then saves to M2M.
	        Uses slug validation to ensure no spaces in tag.

	        """
	        current_blog = BlogPost.objects.get(id=self.blog_id)
	        add_tag = BlogPostTags(tag=self.blog_tag)
	        add_tag.save()
	        add_tag.blog_posts.add(current_blog)
	        return super(BlogPostDetail, self).form_valid(form)
        else:
            messages.error(self.request, 
            	'The tag "{0}" already exists for this post!'.format(self.blog_tag))
            return super(BlogPostDetail, self).form_invalid(form)

    def get_success_url(self):
		""" Returns user to original blog post """
		return reverse('project:detail', kwargs={
			'id': self.kwargs['id'],
			'slug': self.kwargs['slug'],
			})

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class BlogPostCreate(CreateView):
    """ Requires login, and saves to logged in user. """
    form_class = BlogForm
    template_name = 'project/blogpost_form.html'

    def form_valid(self, form):
        """ Attributes blog post to "user" foreignkey from models. """
        form.instance.user = self.request.user
        return super(BlogPostCreate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'This field is required')
        return self.render_to_response(self.get_context_data(form=form))

    def get_queryset(self):
    	""" 
    	Gets user's blog post queryset.
    	Used with below reverse after post is created
    	"""
        user_set = super(BlogPostCreate, self).get_queryset()
        return user_set.filter(user=self.request.user)

    def get_success_url(self):
        return reverse('project:detail', kwargs={
            'id': self.object.id,
            'slug': self.object.slug,
            })

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
		return profile_posts.filter(author=self.author).order_by('-added')

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
        return user_posts.filter(author=self.request.user).order_by('-added')

    def get_context_data(self, **kwargs):
        """ Uses auth'd user as context var to template """
        context = super(UserDashboard, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class BlogTags(ListView):
	""" Lists blog posts with a certain tag """
	model = BlogPostTags
	template_name = 'project/tag_blogs.html'

	def get_context_data(self, **kwargs):
		""" 
		Returns tag name from url to template,
        and queries for posts with tag
        """
		context = super(BlogTags, self).get_context_data(**kwargs)
		self.tag = self.kwargs['tag']
		context['tag'] = self.kwargs['tag']
		context['tagged_posts'] = BlogPost.objects.filter(
			blogposttags__tag=str(self.tag)).order_by('-added')
		return context