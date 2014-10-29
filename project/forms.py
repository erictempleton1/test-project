from django import forms
from project.models import BlogPost, BlogPostTags


class BlogForm(forms.ModelForm):

	class Meta:
		model = BlogPost
		fields = ['title', 'content']
		widgets = {
		'content': forms.Textarea(attrs={'cols': 80, 'rows':20}),
		}

class BlogPostTagsForm(forms.ModelForm):

	class Meta:
		model = BlogPostTags
		fields = ['tag']