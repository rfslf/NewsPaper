from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from django.core.paginator import Paginator
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class PostsList(ListView):
	model = Post  # указываем модель, объекты которой мы будем выводить
	template_name = 'posts.html'  # указываем имя шаблона, в котором будет лежать HTML,
	# в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
	context_object_name = 'posts'  # это имя списка, в котором будут лежать все объекты, его надо указать,
	# чтобы обратиться к самому списку объектов через HTML-шаблон
	queryset = Post.objects.order_by('-id')
	paginate_by = 2  # поставим постраничный вывод в один элемент


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


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
	permission_required = ('news.add_post',)
	template_name = 'post_add.html'
	form_class = PostForm

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса
		if form.is_valid():  # если пользователь ввёл всё правильно и нигде не накосячил, то сохраняем новый товар
			form.save()
		return super().get(request, *args, **kwargs)


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	permission_required = ('news.change_post',)
	template_name = 'post_edit.html'
	form_class = PostForm

	def get_object(self, **kwargs):
		id = self.kwargs.get('pk')
		return Post.objects.get(pk=id)

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса
		if form.is_valid():  # если пользователь ввёл всё правильно и нигде не накосячил, то сохраняем новый товар
			form.save()
		return super().get(request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
	permission_required = ('news.delete_post',)
	template_name = 'post_delete.html'
	queryset = Post.objects.all()
	success_url = '/news/'
