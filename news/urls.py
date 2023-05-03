from django.urls import path
from .views import PostsList, PostDetail, PostSearch, PostCreateView, PostUpdateView, PostDeleteView  # импортируем наше представление

urlpatterns = [
	path('', PostsList.as_view()),
	# т.к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
	path('<int:pk>', PostDetail.as_view(), name='post_detail'),  # pk — это первичный ключ, который будет выводиться у нас в шаблон
	path('search', PostSearch.as_view()),
	path('add/', PostCreateView.as_view(), name='post_create'),
	path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_update') ,
	path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete')

]