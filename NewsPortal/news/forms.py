from django import forms
from django.core.exceptions import ValidationError
from .models import *

class PostForm(forms.ModelForm):
    content = forms.CharField(min_length = 20)
    class Meta:
        model = Post
        fields = [
            'author',
            'category',
            'name',
            'content',
        ]