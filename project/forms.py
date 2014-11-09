from django import forms
from django.forms import ModelForm, CharField
from project.models import BlogPost, BlogPostTags
from django.core.validators import validate_slug
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class BlogForm(forms.ModelForm):

	class Meta:
		model = BlogPost
		fields = ['title', 'content']
		widgets = {
		'content': SummernoteWidget(),
		'title': forms.TextInput(attrs={'size': 75}),
		}

class BlogPostTagsForm(forms.ModelForm):

    tag = CharField(validators=[validate_slug])

    class Meta:
        model = BlogPostTags
        fields = ['tag']