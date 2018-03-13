import json
import re
from datetime import datetime
from math import floor
from django.http import HttpResponse
from django.views.generic.base import View

from Core.models import Configuration, CostCategory, Cost, Tags, History, Archive


class ActionsView(View):

    def POST(self, data):
        return self.request.POST[data]

    @property
    def configuration(self):
        return self.request.user.settings.configurations.all().get(name_url=self.request.POST['name'])

    @staticmethod
    def action_dispatch(**kwargs):

        if len(kwargs) == 3:
            history_for_settings = History(description='<b>' + kwargs['configuration'].name + '</b>: ' + kwargs['description'])
            history_for_configuration = History(description=kwargs['description'])

            history_for_settings.save()
            history_for_configuration.save()

            kwargs['settings'].history.add(history_for_settings)
            kwargs['configuration'].history.add(history_for_configuration)
        else:
            history = History(description=kwargs['description'])
            history.save()
            kwargs['settings'].history.add(history)


class CorrectFreeMoney(ActionsView):

    description_for_action_record = 'Изменена сумма накоплений на <b>%s</b> р.'

    def post(self, *args, **kwargs):
        settings = self.request.user.settings
        value = str(self.POST('value'))
        status = 0

        if re.fullmatch(r'(\+|\-)?\d+', value):
            if self.POST('value').isdigit():
                settings.free_money = int(value)
            elif self.POST('value')[0] == '+':
                settings.free_money += int(value)
            else:
                settings.free_money -= int(value)
            status = 1
            settings.save()
            self.action_dispatch(description=self.description_for_action_record % value, settings=settings)

        response = {'status': status}
        return HttpResponse(json.dumps(response), content_type='application/json')


class CreateNewPlan(ActionsView):

    description_for_action_record = 'Создан новый план распределения бюджета <b style="color:%s"><i class="%s" aria-hidden="true"></i> %s</b>.'

    def post(self, *args, **kwargs):

        configuration = Configuration(name=self.POST('name-plan'), income=self.POST('income'),
                                      icon=self.POST('icon'), color=self.POST('color'))
        configuration.save()
        c = [item[1] for item in self.request.POST.items()][4:]
        for n, item in enumerate(c):
            if n % 2 == 1 and c[n - 1] and c[n]:
                cost_category = CostCategory(name=c[n - 1], max=c[n])
                cost_category.save()
                configuration.category.add(cost_category)
        self.request.user.settings.configurations.add(configuration)
        self.action_dispatch(description=self.description_for_action_record %
                                         (configuration.color, configuration.icon, configuration.name),
                             settings=self.request.user.settings)

        return HttpResponse('ok')


class StartNewPeriod(ActionsView):

    description_for_action_record = 'Начало нового рассчетного периода. На накопительный счет было зачислено <b>%s</b> р. остатка с предыдущего месяца. Все траты перемещены в архив.'

    def post(self, *args, **kwargs):
        # Наша конфигурация
        configuration = self.configuration
        # Значения configuration перед обновлением
        last_income = configuration.income
        last_date = configuration.date
        # Рассчитываем непотраченный остаток с предыдущего месяца
        balance = last_income - sum(
            list(map(lambda x: x.value, Cost.objects.filter(costcategory__configuration=configuration))))
        # Вносим новые правки в план
        configuration.income = int(self.POST('income'))
        configuration.date = datetime.now().date()
        configuration.save()
        # Непотраченный остаток присваиваем к общему счету
        settings = configuration.settings_set.all()[0]
        settings.free_money += balance
        settings.save()
        # Удаляем траты и производим перерасчет максимумов в категориях на основе введенных данных
        count_category = configuration.category.all().count()
        distribution = (int(self.POST('income')) - last_income) / count_category
        if distribution == int(distribution):
            list_values_add = [distribution] * count_category
        else:
            list_values_add = [floor(distribution)] * count_category
            list_values_add[-1] += int(self.POST('income')) - last_income - (floor(distribution) * count_category)

        # Создаем таблицу архива
        archive = Archive(date_one=last_date)
        archive.save()

        # Переменная суммы трат
        amount_cost = 0

        for n, category in enumerate(configuration.category.all()):
            costs = category.cost.all()
            # Перемещаем данные в архив
            archive.archive_costs.add(*[cost for cost in costs])
            # Считаем сумму трат
            amount_cost += sum([cost.value for cost in costs])
            category.cost.clear()
            cat = category
            # Корректируем лимиты категорий
            cat.max += list_values_add[n]
            cat.save()

        # Записываем сумму трат и сэкономленных
        archive.spent = amount_cost
        archive.saved = last_income - amount_cost
        archive.save()

        # Прикрепляем полученный архив в нашей конфгурации
        configuration.archive.add(archive)

        self.action_dispatch(description=self.description_for_action_record % balance,
                             settings=self.request.user.settings, configuration=configuration)

        response = {'status': 1, 'balance': balance}
        return HttpResponse(json.dumps(response), content_type='application/json')


class EditDate(ActionsView):

    description_for_action_record = 'Изменена дата на %s.'

    def post(self, *args, **kwargs):
        date = datetime.strptime(self.POST('date'), '%Y-%m-%d').date()
        status = 0
        if datetime.now().date() >= date:
            configuration = self.configuration
            configuration.date = date
            configuration.save()
            status = 1
        response = {'status': status}

        self.action_dispatch(description=self.description_for_action_record % str(date),
                             settings=self.request.user.settings, configuration=self.configuration)

        return HttpResponse(json.dumps(response), content_type='application/json')


class DeletePlan(ActionsView):

    description_for_action_record = 'План <b>%s</b> был удалён.'

    def post(self, *args, **kwargs):
        balance = self.configuration.income - sum(
            list(map(lambda x: x.value, Cost.objects.filter(costcategory__configuration=self.configuration))))
        settings = self.configuration.settings_set.all()[0]
        settings.free_money += balance
        settings.save()
        # Данные для записи в историю
        name = self.configuration.name

        self.action_dispatch(description=self.description_for_action_record % name,
                             settings=self.request.user.settings)
        try:
            self.configuration.delete()
            status = 1
        except:
            status = 0
        response = {'status': status}

        return HttpResponse(json.dumps(response), content_type='application/json')


class SettingsPlan(ActionsView):

    description_for_action_record = 'План отредактирован'

    def post(self, *args, **kwargs):

        configuration = self.configuration
        configuration.name = self.POST('name-plan')
        configuration.income = self.POST('income')
        configuration.icon = self.POST('icon')
        configuration.color = self.POST('color')
        configuration.save()

        current_category = configuration.category.all()
        number_category = 0
        c = [item[1] for item in self.request.POST.items()][5:]
        for n, item in enumerate(c):
            if n % 2 == 1 and c[n - 1] and c[n]:
                if not (current_category[number_category].name == c[n - 1] and
                        current_category[number_category].max == c[n]):
                    for_save = current_category[number_category]
                    for_save.name = c[n - 1]
                    for_save.max = c[n]
                    for_save.save()
                number_category += 1

        self.action_dispatch(description=self.description_for_action_record,
                             settings=self.request.user.settings, configuration=configuration)

        return HttpResponse('ok')


class ToggleCategoryWeekTable(ActionsView):
    def post(self, *args, **kwargs):
        bool_field = self.configuration.category.all().get(name=self.POST('category'))
        bool_field.included_week_table = not bool_field.included_week_table
        bool_field.save()
        return HttpResponse('ok')


class InputCost(ActionsView):

    description_for_action_record = 'Зафиксирован расход на сумму <b>%s</b> <i class="fa fa-rub" aria-hidden="true"></i>'

    def post(self, *args, **kwargs):
        # Счетчик суммы для записи в историю
        number = 0
        for cat in self.configuration.category.all():
            value = 'value-' + str(cat.id)
            detailed_comment = 'detail-comment-' + str(cat.id)
            n = 0
            while True:
                complete_value = value + '-' + str(n)
                complete_detailed_comment = detailed_comment + '-' + str(n)
                try:
                    cost = Cost(value=self.request.POST[complete_value],
                                detailed_comment=self.request.POST[complete_detailed_comment])
                    number += int(self.request.POST[complete_value])
                except KeyError:
                    break
                cost.save()
                for tag in self.request.POST.getlist('tags'):
                    tag_obj, b = Tags.objects.update_or_create(user=str(self.request.user), name=tag)
                    cost.tags.add(tag_obj)
                cat.cost.add(cost)
                n += 1

        self.action_dispatch(description=self.description_for_action_record % number,
                             settings=self.request.user.settings, configuration=self.configuration)

        return HttpResponse('ok')


class DeleteCost(ActionsView):

    description_for_action_record = 'Удалена трата на сумму <b>%s</b> <i class="fa fa-rub" aria-hidden="true"></i> с комментарием: %s'

    def post(self, *args, **kwargs):
        cost = Cost.objects.filter(costcategory__configuration=self.configuration)\
            .get(id=self.POST('id'))
        value = cost.value
        comment = cost.detailed_comment
        cost.delete()

        self.action_dispatch(description=self.description_for_action_record % (value, comment),
                             settings=self.request.user.settings, configuration=self.configuration)

        return HttpResponse('ok')
