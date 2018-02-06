from datetime import datetime
from django.db import models


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
    cost = models.ManyToManyField(Cost, verbose_name='Траты')
    max = models.IntegerField('Предел затраты')


class Configuration(models.Model):
    """
    При создании конфигурации указывается имя конфигурации, создаются категории, создается экземлпяр истории трат,
    объявляется доход за месяц, и запоминается дата.
    """
    name = models.CharField('Название конфигурации', max_length=100)
    category = models.ManyToManyField(CostCategory, verbose_name='Категории')
    income = models.IntegerField('Деньги в обороте')
    date = models.DateField('Дата ввода', default=datetime.now)


class Settings(models.Model):
    """
    Пользователь заходит и регистрируется. У него создается связь с эзкмпляром Settings
    Далее есть возможность создать конфигурацию контроля бюджета.
    """
    configurations = models.ManyToManyField(Configuration, verbose_name='Конфигурация')
    free_money = models.IntegerField('Свободные деньги')
