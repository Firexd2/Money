from datetime import datetime
from django.db import models
from django.urls import reverse


class ShoppingListItem(models.Model):
    flag = models.BooleanField('Куплено, или нет', default=False)
    name = models.CharField('Название продукта', max_length=100)
    price = models.IntegerField('Цена продукта', blank=True, null=True)
    count = models.IntegerField('Количество', default=1)
    category = models.ForeignKey('CostCategory', verbose_name='Категория', on_delete=models.CASCADE, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Итем шоп-листа'
        verbose_name_plural = 'Итемы шоп-листа'


class ShoppingList(models.Model):
    name = models.CharField('Название шоп-листа', max_length=100)
    item = models.ManyToManyField(ShoppingListItem, verbose_name='Итемы шоп-листа', blank=True)

    def __str__(self):
        try:
            title = '%s: %s' % (self.configuration.first().settings.first().user, self.name)
        except:
            title = '---'
        return title

    class Meta:
        verbose_name = 'Шоп-лист'
        verbose_name_plural = 'Шоп-листы'


class Tags(models.Model):

    name = models.CharField('Название метки', max_length=100)
    user = models.CharField('Пользователь', max_length=100)
    datetime = models.DateTimeField('Время и дата', auto_now=True)

    def __str__(self):
        return '%s: %s' % (self.user, self.name)

    class Meta:
        verbose_name = 'Метка'
        verbose_name_plural = 'Метки'


class History(models.Model):
    description = models.CharField('Описание действия', max_length=300, blank=True)
    datetime = models.DateTimeField('Время и дата', auto_now=True)

    def __str__(self):
        title = '---'
        if self.settings.count():
            title = '%s, %s' % (self.settings.first().user, self.datetime.date())
        return title

    class Meta:
        verbose_name = 'История аккаунта'
        verbose_name_plural = 'Истории аккаунтов'


class Cost(models.Model):

    value = models.IntegerField()
    tags = models.ManyToManyField(Tags, verbose_name='Метки')
    detailed_comment = models.CharField('Подробный комментарий', max_length=100)
    datetime = models.DateTimeField('Время и дата', auto_now=True)

    def __str__(self):
        try:
            name = self.category.first().configuration.first().settings.first().user
            title = '%s: %s' % (name, self.detailed_comment)
        except:
            title = '--'

        return title

    class Meta:
        verbose_name = 'Трата'
        verbose_name_plural = 'Траты'


class Archive(models.Model):

    date_one = models.DateField()
    date_two = models.DateField('Дата ввода', default=datetime.now)
    archive_costs = models.ManyToManyField(Cost, verbose_name='Траты', blank=True)
    spent = models.IntegerField('Потрачено', blank=True, null=True)
    saved = models.IntegerField('Сэкономлено', blank=True, null=True)
    income = models.IntegerField('Всего', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('detail_archive', args=[str(self.pk)])

    def __str__(self):
        return 'План: %s' % (self.configuration.first().name if self.configuration.first().settings.count() else '---')

    class Meta:
        verbose_name = 'Архив'
        verbose_name_plural = 'Архив'


class CostCategory(models.Model):

    name = models.CharField('Название', max_length=100)
    cost = models.ManyToManyField(Cost, related_name='category', verbose_name='Траты', blank=True)
    included_week_table = models.BooleanField('Включение в недельную таблицу', default=True)
    max = models.IntegerField('Предел затраты')

    def __str__(self):
        try:
            username = self.configuration.first().settings.first().user
            configuration_name = self.configuration.first().name
            title = '{Имя: %s}, {План: %s}, {Категория: %s}' % (username, configuration_name, self.name)
        except:
            title = '---'

        return title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Configuration(models.Model):

    name = models.CharField('Название конфигурации', max_length=100)
    category = models.ManyToManyField(CostCategory, related_name='configuration', verbose_name='Категории')
    income = models.IntegerField('Деньги в обороте')
    icon = models.CharField('Иконка на главной', max_length=100)
    color = models.CharField('Цвет иконки', max_length=20)
    history = models.ManyToManyField(History, related_name='plan_history', blank=True)
    archive = models.ManyToManyField(Archive, related_name='configuration', blank=True)
    shopping_list = models.ManyToManyField(ShoppingList, related_name='configuration', verbose_name='Списки покупок', blank=True)
    date = models.DateField('Дата ввода', default=datetime.now)

    def get_absolute_url(self):
        return reverse('base', args=[str(self.name)])

    def __str__(self):
        name = self.settings.first().user.username if self.settings.count() else '--'
        return '%s: %s' % (name, self.name)

    class Meta:
        verbose_name = 'План распределения бюджета'
        verbose_name_plural = 'Планы распределения бюджета'


class Settings(models.Model):

    configurations = models.ManyToManyField(Configuration, related_name='settings', verbose_name='Конфигурация')
    free_money = models.IntegerField('Свободные деньги', default=0)
    history = models.ManyToManyField(History, related_name='settings', blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Пользовательская настройка'
        verbose_name_plural = 'Пользовательские настройки'


class HelpText(models.Model):
    position = models.CharField('Позиция', max_length=100)
    text = models.TextField('Пояснительный текст')

    def __str__(self):
        return self.position

    class Meta:
        verbose_name = 'Информационная система'
        verbose_name_plural = 'Информационная система'


class VersionControl(models.Model):
    version = models.CharField('Наименование версии', max_length=20)
    description = models.TextField('Описание изменений')
    date = models.DateField('Дата', auto_now_add=True)

    def __str__(self):
        return self.version

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Список версий'
