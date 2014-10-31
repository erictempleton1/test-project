from django import forms
from django.forms import ModelForm, CharField
from project.models import BlogPost, BlogPostTags
from django.core.validators import validate_slug

class BlogForm(forms.ModelForm):

	class Meta:
		model = BlogPost
		fields = ['title', 'content']
		widgets = {
		'content': forms.Textarea(attrs={'cols': 80, 'rows':20}),
		}

class BlogPostTagsForm(forms.ModelForm):

    tag = CharField(validators=[validate_slug])

    class Meta:
        model = BlogPostTags
        fields = ['tag']