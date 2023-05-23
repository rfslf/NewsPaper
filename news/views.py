from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, User, Category
from .filters import PostFilter
from django.core.paginator import Paginator
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.cache import cache # импортируем наш кэш


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
	queryset = Post.objects.all()

	def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
		# Кэш очень похож на словарь, и метод get действует также. Он забирает значение по ключу,
		# если его нет, то забирает None.
		obj = cache.get(f'post-{self.kwargs["pk"]}', None)
		# если объекта нет в кэше, то получаем его и записываем в кэш
		if not obj:
			obj = super().get_object(queryset=self.queryset)
			cache.set(f'post-{self.kwargs["pk"]}', obj)
		return obj


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
		if form.is_valid():
			# отправляем письмо ['post_type', 'header', 'body', 'author', 'category']
			# send_mail(
			# subject=request.POST['header'],
			# message=request.POST['body'],
			# message=form,
			# from_email='avdonin@unn.ru',
			# recipient_list=['rocknroll@mail.ru']
			# )
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


@login_required
def subscribe_me(request):
	user = request.user  # получаем из request самого пользователя
	cat_id = request.POST['cat_id']  # получаем из request то, что пришло из формы через POST
	category = Category.objects.get(pk=int(cat_id))  # получаем категорию через cat_id
	if user not in category.subscriber.all():
		# Добавляем пользователя в связь с категорией
		category.subscriber.add(user)
	# Если связь уже есть, то отписываем, т.е. удаляем из этой связи
	else:
		category.subscriber.remove(user)
	return redirect(request.headers['Referer'])
