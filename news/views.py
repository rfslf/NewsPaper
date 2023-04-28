from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post
from .filters import PostFilter
from django.core.paginator import Paginator


class PostsList(ListView):
	model = Post  # указываем модель, объекты которой мы будем выводить
	template_name = 'posts.html'  # указываем имя шаблона, в котором будет лежать HTML,
	# в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
	context_object_name = 'posts'  # это имя списка, в котором будут лежать все объекты, его надо указать,
	# чтобы обратиться к самому списку объектов через HTML-шаблон
	queryset = Post.objects.order_by('-id')
	paginate_by = 10  # поставим постраничный вывод в один элемент


# создаём представление, в котором будут детали конкретного отдельного товара
class PostDetail(DetailView):
	model = Post
	template_name = 'post.html'
	context_object_name = 'post'


class PostSearch(ListView):
	model = Post
	template_name = 'posts_search.html'
	context_object_name = 'post'
	ordering = ['-id']

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр
		return context
