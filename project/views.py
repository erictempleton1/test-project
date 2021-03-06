from collections import Counter
from django.contrib import messages
from django.shortcuts import redirect
from haystack.views import SearchView
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from registration.backends.simple.views import RegistrationView
from project.models import BlogPost, BlogPostTags, UserProfile
from django.shortcuts import get_list_or_404, get_object_or_404
from project.forms import (BlogForm, BlogPostTagsForm, UserRegistrationForm,
                    LoginUserForm)
from django.views.generic import (ListView, CreateView, DetailView,
                    UpdateView, DeleteView, TemplateView, FormView,
                    View)

class HomePageView(ListView):
    """ Lists all blog posts for every user. """
    model = BlogPost
    template_name = 'project/index.html'
    context_object_name = 'all_posts'
    paginate_by = 10

    def get_queryset(self):
        """ All posts sorted by date added """
        all_posts = super(HomePageView, self).get_queryset()
        return all_posts.order_by('-added')

    def get_context_data(self, **kwargs):
        """
        Returns all tags, and used item_count to sort by popular.
        Also returns top 5 most popular posts based on hits.
        """
        context = super(HomePageView, self).get_context_data(**kwargs)
        get_tags = BlogPostTags.objects.all()
        context['tag_count'] = self.item_count(get_tags)
        context['popular_posts'] = BlogPost.objects.all().order_by('-hits')[:5]
        return context

    def item_count(self, tags):
    	""" Creates tuple of tags by most popular, and provides count """
        clean_tags = [str(tag) for tag in tags]
        c = Counter(clean_tags)
        return c.most_common()

class RegistrationRedirect(RegistrationView):
    """
    Overrides default django-reg redirect
    and returns new user to homepage.
    """
    form_class = UserRegistrationForm

    def get_success_url(self, request, user):
        return reverse('project:homepage')

class AboutPageView(TemplateView):
	""" Basic About page """
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
        current_post = BlogPost.objects.get(id=self.id)
        context['blog_post'] = current_post
        context['tags'] = BlogPost.objects.get(
            id=self.id).blogposttags_set.all()

        # works for now, but makes more queries than preferred
        # need to revisit later
        context['blog_post'].hits += 1
        context['blog_post'].save()

        """
        Checks if favorite exists already.
        Un-auth'd user has no user object, so typeerror exists.
        Catching the error below forces un-auth'd user to login or reg
        if they click fav, and allows the page to load.
        """
        try:
            me, created = UserProfile.objects.get_or_create(
                user=self.request.user)
            if current_post in me.favorites.all():
                context['favorite_exists'] = True
            else:
                context['favorite_exists'] = False
        except TypeError:
            context['favorite_exists'] = False

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
            messages.error(
                self.request,
                'The tag "{0}" already exists for this post!'.format(
                    self.blog_tag))
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
        messages.error(self.request, 'Both fields are required')
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

class ProfileBlog(ListView):
    """ Lists all posts by specific user """
    model = BlogPost
    template_name = 'project/profile_blog.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileBlog, self).get_context_data(**kwargs)
        context['author_posts'] = BlogPost.objects.filter(
            author=self.kwargs['author'])
        context['author'] = self.kwargs['author']
        
        # get or user and author objects
        user_follow, user_created = User.objects.get_or_create(
            username=self.kwargs['author'])
        
        # return following/follower count
        user_follows, created = UserProfile.objects.get_or_create(user=user_follow)
        context['all_following'] = user_follows.following.all()
        context['all_followers'] = user_follows.followers.all()

        try:
            # check if user is already following the author
            me, created_me = UserProfile.objects.get_or_create(
                user=self.request.user)
            context['follow_exists'] = me.following.filter(
                user=user_follow).exists()
        except TypeError:
            # users not logged in raise TypeError
            # self.request.user does not exist for users not logged in
            context['follow_exists'] = None

        return context


class BlogPostUpdate(UpdateView):
	""" Requires login, and only post author can edit. """
	model = BlogPost
	form_class = BlogForm

	def get_queryset(self):
		""" 
		Overrides default queryset to only allow post creator
		to update, and raises 404 error otherwise.
		"""
		user_set = BlogPost.objects.filter(id=self.kwargs['id'])
		return user_set.filter(user=self.request.user)

	def get_success_url(self):
		return reverse('project:detail', kwargs={
			'id': self.object.id,
			'slug': self.object.slug,
			})

class BlogPostDelete(DeleteView):
    """ Requires login, and only post author can delete """
    model = BlogPost
    success_url = reverse_lazy('project:user_dashboard')

    def get_queryset(self):
        """
        Query by id instead of slug to
        avoid duplicate issues.
        """
        messages.success(self.request, 'Post deleted')
        user_set = BlogPost.objects.filter(id=self.kwargs['id'])
        return user_set.filter(user=self.request.user)

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

class UserFollowers(ListView):
    """ Lists all followers for a given user """
    model = UserProfile
    template_name = 'project/user_followers.html'

    def get_context_data(self, **kwargs):
       context = super(UserFollowers, self).get_context_data(**kwargs)
       context['author'] = self.kwargs['author']

       # get author object
       user_follow = get_object_or_404(User, username=self.kwargs['author'])

       # return author's followers
       user_follows = get_object_or_404(UserProfile, user=user_follow)
       all_followers = user_follows.followers.all()
       context['all_followers'] = all_followers
       return context

class UserFollowing(ListView):
    """ Lists all users a user is following """
    model = UserProfile
    template_name = 'project/user_following.html'

    def get_context_data(self, **kwargs):
        context = super(UserFollowing, self).get_context_data(**kwargs)
        context['author'] = self.kwargs['author']

        # get author objects
        user_follow = get_object_or_404(
            User,
            username=self.kwargs['author']
            )

        # return users author is following
        user_follows = get_object_or_404(UserProfile, user=user_follow)
        all_following = user_follows.following.all()
        context['all_following'] = all_following
        return context

class UserFeed(ListView):
    """
    Creates a user feed based on 
    users followed.
    A little inefficient at the moment,
    need to look into better way to query.
    """
    model = UserProfile
    template_name = 'project/user_feed.html'

    def get_context_data(self, **kwargs):
        context = super(UserFeed, self).get_context_data(**kwargs)
        user_follows = get_object_or_404(UserProfile, user=self.request.user)
        all_following = user_follows.following.all().prefetch_related('following')

        # bottleneck here
        user_names = [items.user.username for items in all_following]
        
        context['f_posts'] = BlogPost.objects.filter(
            author__in=user_names).order_by('-added')
        return context

class FollowUser(View):
    """ 
    Follow a specific user, and not yourself
    get_or_create returns a tuple with true or false
    """
    model = UserProfile

    def get(self, request, author):

        # get or create user and author objects
        me, me_created = UserProfile.objects.get_or_create(user=request.user)
        user_follow = get_object_or_404(User, username=str(author))

        # check if user is already following the author
        follow_exists = me.following.filter(user=user_follow).exists()

        # exists check, and check to not follow self
        if follow_exists or request.user.username == author:
            return redirect('/{}'.format(author))
        else:
            add_user = get_object_or_404(UserProfile, user=user_follow)
            me.following.add(add_user)
            return redirect('/{}'.format(author))

class UnfollowUser(View):
    """
    Unfollow a user, which uses similar approach to FollowUser.
    Uses get_object_or_404 instead of get_or_create,
    so extra instances aren't created.
    """
    model = UserProfile

    def get(self, request, author):
        me = get_object_or_404(UserProfile, user=request.user)
        user_follow = get_object_or_404(User, username=str(author))
        follow_exists = me.following.filter(user=user_follow).exists()

        if follow_exists and request.user.username != author:
            remove_user = get_object_or_404(UserProfile, user=user_follow)
            me.following.remove(remove_user)
            return redirect('/{}'.format(author))
        else:
            return redirect('/{}'.format(author))

class FavoritePost(View):
    """
    Saves current post to favorites list.
    Duplicate favorites not saved.
    """
    model = UserProfile

    def get(self, request, id, slug):
        me, me_created = UserProfile.objects.get_or_create(user=request.user)
        post_fav = get_object_or_404(BlogPost, id=id)
        me.favorites.add(post_fav)
        return redirect('/{0}/{1}'.format(id, slug))

class UnfavoritePost(View):
    """ Removes current post from favorites list. """
    model = UserProfile

    def get(self, request, id, slug):
        me, me_created = UserProfile.objects.get_or_create(user=request.user)
        post_unfav = get_object_or_404(BlogPost, id=id)
        me.favorites.remove(post_unfav)
        return redirect('/{0}/{1}'.format(id, slug))

class FavsView(ListView):
    """List all posts a user has favorited"""
    model = UserProfile
    template_name = 'project/user_fav.html'

    def get_context_data(self, **kwargs):
        context = super(FavsView, self).get_context_data(**kwargs)
        current_author = get_object_or_404(
            User,
            username=self.kwargs['author']
            )
        author_favs, created = UserProfile.objects.get_or_create(
            user=current_author)
        context['author_favs'] = author_favs.favorites.all()
        context['author'] = self.kwargs['author']
        return context

# notes:
#
# regex issue in urls.py exists-
#     username with number goes to post
#     example: /eric1/favorites
#
# following feed-
# user_names = [items.user.username for items in all_following]
# f_posts = BlogPost.objects.filter(author__in=user_names).order_by('-added')
