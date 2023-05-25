from django.db.models.signals import m2m_changed  # Нужен для ManyToMany
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import PostCategory


# Для декоратора передаётся первым аргументом сигнал, \
# на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, **kwargs):
	header = instance.header
	message = instance.body
	post = instance
	# subscribers_email_list = []
	if kwargs['action'] == "post_add":
		categories = instance.category.all()
		for category in categories:
			subscribers = category.subscriber.all()
			for subscriber in subscribers:
				html_content = render_to_string(
					'email.html',
					{'subject': header, 'message': message, 'username': subscriber.username, 'post': post})
				msg = EmailMultiAlternatives(
					subject=f'Новая статья на сайте NewsPapers',
					body=f'Содержание: {message}',  # это то же, что и message
					from_email='avdonin@unn.ru',
					to=[subscriber.email],
				)
				msg.attach_alternative(html_content, "text/html")  # добавляем html
				print(html_content)  # проверка содержимого отправки
			# 	нужно отключить для реальной отправки
			#   msg.send()
