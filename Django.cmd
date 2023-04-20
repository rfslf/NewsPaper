# 1. Создать двух пользователей (с помощью метода User.objects.create_user).
from django.contrib.auth.models import User
user1 = User.objects.create_user("batman", "batman@dc.com", "brucewayne")
user2 = User.objects.create_user("superman", "superman@dc.com", "clarkkent")
user3 = User.objects.create_user("robin", "robin@dc.com", "johnblake")
# user1 = User.objects.get(username="batman")
# user2 = User.objects.get(username="superman")

# 2. Создать два объекта модели Author, связанные с пользователями.
from news.models import Author
author1 = Author.objects.create(author=user1)
author2 = Author.objects.create(author=user2)
# author3 = Author.objects.create(author=user3)
# author3.delete()

# 3. Добавить 4 категории в модель Category.
from news.models import Category
category1 = Category.objects.create(category='crime')
category2 = Category.objects.create(category='news')
category3 = Category.objects.create(category='superpower')
category4 = Category.objects.create(category='health')

# 4. Добавить 2 статьи и 1 новость.
from news.models import Post
news1 = Post.objects.create(post_type='N', header='Bank robbery', body='Gotham bank robed for 1M$', author=author1)
post1 = Post.objects.create(header='Heat vision', body='Superman can project beams of heat from his eyes which are hot enough to melt steel.', author=author2)
post2 = Post.objects.create(header='Human powers', body ='Batman relies on "his own scientific knowledge, detective skills, and athletic prowess".', author=author1)

# 5. Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
from news.models import PostCategory
news1.category.add(category1, category2)
post1.category.add(category3)
post2.category.add(category3, category4)

# 6. Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).
from news.models import Comment
comment1 = Comment.objects.create(comment='Bastards must be punished...', post=news1, user=user3)
comment2 = Comment.objects.create(comment='Reveal Bat-Signal!', post=news1, user=user2)
comment3 = Comment.objects.create(comment='You were never a God. You were never even a man.', post=post1, user=user1)
comment4 = Comment.objects.create(comment='The point was that Batman could be anyone.', post=post2, user=user3)
comment5 = Comment.objects.create(comment='A hero can be anyone.', post=post2, user=user1)

# 7. Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
# В задании нет требований к лайкам/дизлайкам. Условимся, user может проставить единожды только 1 реакцию и не себе.
comment1.like() # user1
comment1.like() # user2
comment2.like() # user3
comment3.like() # user3
comment3.dislike() # user2
comment4.dislike() # user1
comment5.like() # user2
comment5.like() # user3
post1.dislike() # user1
post2.like() # user2
post2.like() # user3

# 8. Обновить рейтинги пользователей.
#       Он состоит из следующего:
#           суммарный рейтинг каждой статьи автора умножается на 3;
#           суммарный рейтинг всех комментариев автора;
#           суммарный рейтинг всех комментариев к статьям автора
from django.db.models import Sum
author1_old_rating = author1.user_rating
author1_delta_rating = Post.objects.filter(author = author1).aggregate(Sum("post_rating"))['post_rating__sum']*3 + \
Comment.objects.filter(user = author1.author).aggregate(Sum("comment_rating"))['comment_rating__sum'] + \
Comment.objects.filter(post__in=Post.objects.filter(author = author1)).aggregate(Sum("comment_rating"))['comment_rating__sum']
author1_new_rating = author1_old_rating + author1_delta_rating
author1.update_rating(author1_new_rating)

author2_old_rating = author2.user_rating
author2_delta_rating = Post.objects.filter(author=author2).aggregate(Sum("post_rating"))['post_rating__sum']*3 + \
Comment.objects.filter(user=author2.author).aggregate(Sum("comment_rating"))['comment_rating__sum'] + \
Comment.objects.filter(post__in=Post.objects.filter(author=author2)).aggregate(Sum("comment_rating"))['comment_rating__sum']
author2_new_rating = author2_old_rating + author2_delta_rating
author2.update_rating(author2_new_rating)

# 9. Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
top_author = Author.objects.all().order_by('-user_rating').first()
print(f'Top rating is {top_author.user_rating} by user {top_author.author}')

# 10. Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
# Post.objects.all().values('create_time', 'author_id', 'post_rating', 'header', 'body').order_by('-post_rating').first()
top_post = Post.objects.all().order_by('-post_rating').first()
print(f'Date:{top_post.create_time}; author:{top_post.author.author};rating:{top_post.post_rating};{top_post.header};{top_post.preview()}')

# 11. Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
Comment.objects.filter(post=top_post).values('comment_time', 'user', 'comment_rating', 'comment')