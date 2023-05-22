import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from datetime import datetime
from news.models import Category, Post
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def weekly_summery():
	# Проверка рассылки, нужно прятать на рабочем сервере
	print('Hello from Django! This is weekly summery job.')

	for category in Category.objects.all():
		news_from_each_category = []
		# определение номера прошлой недели
		week_number_last = datetime.now().isocalendar()[1] - 1
		posts = Post.objects.filter(create_time__week=week_number_last, category=category)
		for news in posts:
			# преобразуем дату в человеческий вид
			date_format = news.create_time.strftime("%m/%d/%Y")
			# из данных запроса выдираем нужные нам поля, и из значений данных
			# полей формируем заголовок и реальную ссылку на переход на статью на наш сайт
			new = f'http://127.0.0.1:8000/news/{news.pk} {news.header} публикация {date_format}'
			# каждую строчку помещаем в список новостей
			news_from_each_category.append(new)
		# Проверка рассылки, нужно прятать на рабочем сервере
		print("Письма будут отправлены следующим подписчикам категории:", category.category, '( id:', category.id, ')')

		# переменная subscribers содержит информацию по подписчиках, в дальнейшем понадобится их адрес
		subscribers = category.subscriber.all()
		for subscriber in subscribers:
			# Проверка рассылки, нужно прятать на рабочем сервере
			print('____________________________', subscriber.email, '___________________________________')
			html_content = render_to_string(
				'weekly_summery.html',
				{'user': subscriber, 'text': news_from_each_category, 'category_name': category.category,
					'week_number_last': week_number_last})

			msg = EmailMultiAlternatives(
				subject=f'Здравствуй, {subscriber}, новые статьи за прошлую неделю в вашем разделе!',
				from_email='avdonin@unn.ru',
				to=[subscriber.email]
			)
			msg.attach_alternative(html_content, 'text/html')

			# Проверка рассылки, нужно прятать на рабочем сервере
			print(html_content)
			# Что бы запустить реальную рассылку нужно убрать комментирование
			# msg.send()


# Функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
	"""This job deletes all apscheduler job executions older than `max_age` from the database."""
	DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
	help = "Runs apscheduler."

	def handle(self, *args, **options):
		scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
		scheduler.add_jobstore(DjangoJobStore(), "default")

		# добавляем работу нашему задачнику
		scheduler.add_job(
			weekly_summery,
			# для проверки отправки временно задано время срабатывания каждую четную минуту
			# для production trigger=CronTrigger(week='*')
			trigger=CronTrigger(minute="*/2"),
			# То же самое что и интервал, но задача триггера таким образом более понятна django
			id="weekly_summery",  # уникальный ИД
			max_instances=1,
			replace_existing=True,
		)
		logger.info("Added job 'weekly_summery'.")

		scheduler.add_job(
			delete_old_job_executions,
			trigger=CronTrigger(
				day_of_week="mon", hour="00", minute="00"
			),
			# Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
			id="delete_old_job_executions",
			max_instances=1,
			replace_existing=True,
		)
		logger.info(
			"Added weekly job: 'delete_old_job_executions'."
		)

		try:
			logger.info("Starting scheduler...")
			scheduler.start()
		except KeyboardInterrupt:
			logger.info("Stopping scheduler...")
			scheduler.shutdown()
			logger.info("Scheduler shut down successfully!")
