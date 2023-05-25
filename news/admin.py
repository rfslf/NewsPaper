from django.contrib import admin
from .models import Post, Comment, Category, SubscriberCategory

# создаём новый класс для представления товаров в админке
class PostAdmin(admin.ModelAdmin):
    # list_display - это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('id', 'header', 'body', 'author', 'post_rating',)
    list_filter = ('category', 'author')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('header',)  # тут всё очень похоже на фильтры из запросов в базу



admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(SubscriberCategory)