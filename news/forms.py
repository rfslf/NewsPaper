from django.forms import ModelForm
from .models import Post, Category


class PostForm(ModelForm):
	class Meta:
		model = Post
		fields = ['post_type', 'header', 'body', 'author', 'category']


