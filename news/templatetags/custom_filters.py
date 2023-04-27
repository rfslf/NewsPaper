from django import template
import re

register = template.Library()  # если мы не зарегистрируем наши фильтры,
# то django никогда не узнает где именно их искать и фильтры потеряются


@register.filter(name='censor')
def censor(value):
    if isinstance(value, str):
        # проверяем, что ищем в строке
        STOP_WORDS = ['damn', 'ass', ]
        for word in STOP_WORDS:
            insensitive_word = re.compile(word, re.IGNORECASE)
            value = insensitive_word.sub('<*>', value)
        return value
    else:
        raise ValueError(f'Нельзя цензурировать не строку')
    # в случае, если кто-то неправильно воспользовался нашим фильтром, выводим ошибку
