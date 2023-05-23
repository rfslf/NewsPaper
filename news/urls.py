from django.urls import path
# импортируем наше представление
from .views import PostsList, PostDetail, PostSearch, PostCreateView, PostUpdateView, PostDeleteView
from .views import subscribe_me
# from django.views.decorators.cache import cache_page

urlpatterns = [
	path('', PostsList.as_view()),
	# т.к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
	# pk — это первичный ключ, который будет выводиться у нас в шаблон
	# path('<int:pk>', cache_page(60*5)(PostDetail.as_view()), name='post_detail'),
	path('<int:pk>', PostDetail.as_view(), name='post_detail'),
	path('search', PostSearch.as_view()),
	path('add/', PostCreateView.as_view(), name='post_create'),
	path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_update') ,
	path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
	path('subscribe/', subscribe_me, name='subscribe'),
]