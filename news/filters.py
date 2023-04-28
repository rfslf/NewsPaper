from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
	class Meta:
		model = Post
		fields = {
			'create_time': ['date__gt'],
			'header': ['icontains'],
			'author': ['exact'],
		}
