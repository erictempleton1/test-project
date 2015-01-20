from django import forms
from django.forms import ModelForm, CharField
from project.models import BlogPost, BlogPostTags
from django.core.validators import validate_slug
from registration.forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class BlogForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """ Override init to set required status """
        super(BlogForm, self).__init__(*args, **kwargs)
        self.fields['content'].required = True
        self.fields['title'].required = True

    class Meta:
        model = BlogPost
        fields = ['title', 'content']
        widgets = {
        'content': SummernoteWidget(),
        'title': forms.TextInput(attrs={'class': 'form-control',
                                        'placeholder': 'Title',}),
        }

class BlogPostTagsForm(forms.ModelForm):

    tag = CharField(validators=[validate_slug])

    class Meta:
        model = BlogPostTags
        fields = ['tag']
        
        
class UserRegistrationForm(RegistrationForm):
    """
    Subclass of RegistrationForm to add bootstrap
    components to reg form
    """
    username = forms.RegexField(
        regex=r'^\w+$',
        max_length=30,
        widget=forms.TextInput(
            attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            }
    ))

    email = forms.CharField(widget=forms.TextInput(
        attrs={
        'class': 'form-control',
        'placeholder': 'Email',
        }
    ))

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        }
    ))

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
        'class': 'form-control',
        'placeholder': 'Password (again)',
        }
    ))

class LoginUserForm(AuthenticationForm):

    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(
            attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            }
    ))