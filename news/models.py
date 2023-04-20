from django.db import models
from django.contrib.auth.models import User

# Create your models here.


#       Модель Author, содержащая объекты всех авторов. Имеет следующие поля:
#           связь «один к одному» с встроенной моделью пользователей User;
#           рейтинг пользователя. Ниже будет дано описание того, как этот рейтинг можно посчитать.
#       Метод update_rating() модели Author, который обновляет рейтинг пользователя, переданный в аргумент этого метода.
class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def update_rating(self, value):
        self.user_rating = int(value)
        self.save()


#        Модель Category. Категории новостей/статей — темы, которые они отражают (спорт, политика, образование и т. д.).
#        Имеет единственное поле: название категории. Поле должно быть уникальным
#        (в определении поля необходимо написать параметр unique = True).
class Category(models.Model):
    category = models.TextField(unique=True)


#        Модель Post, должна содержать в себе статьи и новости, которые создают пользователи.
#        Каждый объект может иметь одну или несколько категорий.
#        Соответственно, модель должна включать следующие поля:
#                связь «один ко многим» с моделью Author;
#                поле с выбором — «статья» или «новость»;
#                автоматически добавляемая дата и время создания;
#                связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
#                заголовок статьи/новости;
#                текст статьи/новости;
#                рейтинг статьи/новости.
#        Методы like() и dislike() в моделях Comment и Post, которые увеличивают/уменьшают рейтинг на единицу.
#        Метод preview() модели Post, который возвращает начало статьи (предварительный просмотр) длиной 124 символа
#        и добавляет многоточие в конце.
class Post(models.Model):
    post = 'P'
    news = 'N'
    TYPES = [(post, 'статья'), (news, 'новость'), ]
    create_time = models.DateTimeField(auto_now_add=True)
    post_type = models.CharField(max_length=255, choices=TYPES, default=post)
    header = models.CharField(max_length=255)
    body = models.TextField()
    post_rating = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return self.body[:124] + '...'


#        Модель PostCategory. Промежуточная модель для связи «многие ко многим»:
#           связь «один ко многим» с моделью Post;
#           связь «один ко многим» с моделью Category.
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


#        Модель Comment. Под каждой новостью/статьёй можно оставлять комментарии,
#        поэтому необходимо организовать их способ хранения тоже. Модель будет иметь следующие поля:
#           связь «один ко многим» с моделью Post;
#           связь «один ко многим» со встроенной моделью User (комментарии может оставить любой пользователь,
#           необязательно автор);
#           текст комментария;
#           дата и время создания комментария;
#           рейтинг комментария.
#        Методы like() и dislike() в моделях Comment и Post, которые увеличивают/уменьшают рейтинг на единицу.
class Comment(models.Model):
    comment = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
