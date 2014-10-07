# add forms here
from django import forms
from project.models import Post

class BlogForm(forms.BaseModelForm):

	class Meta:
		model = Post
		fields = ('title', 'author', 'content')

