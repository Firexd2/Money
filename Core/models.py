from datetime import datetime
from django.db import models
from django.urls import reverse

DICT_LETTERS = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'ye', 'ё': 'yo', 'ж': 'zh', 'з': 'z',
                'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
                'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
                'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', ' ': '_', '-': '_', ',': '_',
                '"': '_', '(': '_', ')': '_', '№': '_'}


class Cost(models.Model):
    """
    Траты
    """
    value = models.IntegerField()
    comment = models.CharField('Комментарий траты', max_length=100)
    datetime = models.DateTimeField('Время и дата', auto_now=True)


class CostCategory(models.Model):
    """
    При внесении трат идет прибавка текущего значения
    """
    name = models.CharField('Название', max_length=100)
    cost = models.ManyToManyField(Cost, verbose_name='Траты', blank=True)
    max = models.IntegerField('Предел затраты')


class Configuration(models.Model):
    """
    При создании конфигурации указывается имя конфигурации, создаются категории, создается экземлпяр истории трат,
    объявляется доход за месяц, и запоминается дата.
    """
    name = models.CharField('Название конфигурации', max_length=100)
    name_url = models.CharField('URL', max_length=120, blank=True, null=True)
    category = models.ManyToManyField(CostCategory, verbose_name='Категории')
    income = models.IntegerField('Деньги в обороте')
    icon = models.CharField('Иконка на главной', max_length=100)
    color = models.CharField('Цвет иконки', max_length=20)
    date = models.DateField('Дата ввода', default=datetime.now)

    def save(self, *args, **kwargs):
        self.name_url = ''
        for letter in self.name.lower():
            try:
                self.name_url += DICT_LETTERS[letter]
            except:
                self.name_url += letter

        super(Configuration, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('conf', args=[str(self.name_url)])


class Settings(models.Model):
    """
    Пользователь заходит и регистрируется. У него создается связь с эзкмпляром Settings
    Далее есть возможность создать конфигурацию контроля бюджета.
    """
    configurations = models.ManyToManyField(Configuration, verbose_name='Конфигурация')
    free_money = models.IntegerField('Свободные деньги', default=0)

    # def __str__(self):
    #     return 'TEST'
