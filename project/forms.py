from django import forms
from django.db import models
from project.models import Post

class CreateForm(forms.ModelForm):

	title = forms.CharField(max_length=100)
	author = forms.CharField(max_length=100)
	body = forms.CharField(widget=forms.Textarea)