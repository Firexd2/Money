from datetime import datetime
from django.db import models

DICT_LETTERS = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'ye', 'ё': 'yo', 'ж': 'zh', 'з': 'z',
                'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
                'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
                'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', ' ': '_', '-': '_', ',': '_',
                '"': '_', '(': '_', ')': '_', '№': '_'}

CHOICES_ICON = (('fa fa-cogs', 'Шестерёнки'),
                ('fa fa-user-o', 'Юзер'),
                ('fa fa-ravelry', 'Равелри'),
                ('fa fa-eercast', 'Оркаст'),
                ('fa fa-at', 'Электронная собака'),
                ('fa fa-bolt', 'Молния'),
                ('fa fa-check', 'Галка'),
                ('fa fa-sun-o', 'Солнце'),
                ('fa fa-credit-card', 'Кредитная карта'),
                ('fa fa-money', 'Доллар'),
                ('fa fa-rub', 'Рубль'))

CHOICES_COLOR_ICON = (('red', 'Красный'),
                      ('blue', 'Синий'),
                      ('yellow', 'Желтый'),
                      ('black', 'Черный'),
                      ('blueviolet', 'Фиолетовый'),
                      ('darkorange', 'Оранжевый'),
                      ('green', 'Зеленый'))


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
    icon = models.CharField('Иконка на главной', max_length=100, choices=CHOICES_ICON)
    color = models.CharField('Цвет иконки', max_length=20, choices=CHOICES_COLOR_ICON)
    date = models.DateField('Дата ввода', default=datetime.now)

    def save(self, *args, **kwargs):
        self.name_url = ''
        for letter in self.name:
            try:
                self.name_url += DICT_LETTERS[letter]
            except:
                self.name_url += letter
        super(Configuration, self).save(*args, **kwargs)


class Settings(models.Model):
    """
    Пользователь заходит и регистрируется. У него создается связь с эзкмпляром Settings
    Далее есть возможность создать конфигурацию контроля бюджета.
    """
    configurations = models.ManyToManyField(Configuration, verbose_name='Конфигурация')
    free_money = models.IntegerField('Свободные деньги', default=0)

    # def __str__(self):
    #     return 'TEST'
