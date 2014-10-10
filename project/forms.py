# add forms here
from django import forms
from project.models import BlogPost

class BlogForm(forms.ModelForm):

	class Meta:
		model = BlogPost
		fields = ['title', 'content']
		widgets = {
		'content': forms.Textarea(attrs={'cols': 80, 'rows':20}),
		}


