import json
from datetime import datetime
from math import floor
from django.http import HttpResponse
from django.views.generic.base import View
from Core.models import Configuration, CostCategory, Cost, Tags, History, Archive, ShoppingList, ShoppingListItem


class ActionsView(View):

    def take_money(self, value):
        settings = self.request.user.settings
        settings.free_money -= int(value)
        settings.save()

    def add_money(self, value):
        settings = self.request.user.settings
        settings.free_money += int(value)
        settings.save()

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


class AddIncome(ActionsView):

    description_for_action_record = 'Добавлен доход на сумму <b>%s</b> р. Комментарий: <b>%s</b>'

    def post(self, *args, **kwargs):
        self.add_money(self.POST('number'))
        self.action_dispatch(description=self.description_for_action_record % (self.POST('number'), self.POST('comment')),
                             settings=self.request.user.settings)
        return HttpResponse('ok')


class TakeIncome(ActionsView):

    description_for_action_record = 'Со счета неиспользованных денег было изъято <b>%s</b> р. Комментарий: <b>%s</b>'

    def post(self, *args, **kwargs):
        self.take_money(self.POST('number'))
        self.action_dispatch(description=self.description_for_action_record % (self.POST('number'), self.POST('comment')),
                             settings=self.request.user.settings)
        return HttpResponse('ok')


class CreateNewPlan(ActionsView):

    description_for_action_record = 'Создан новый план распределения бюджета <b style="color:%s"><i class="%s" aria-hidden="true"></i> %s</b>.'

    def post(self, *args, **kwargs):

        self.take_money(int(self.POST('income')))

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

    description_for_action_record = 'Начало нового рассчетного периода. На счет неиспользованных денег было зачислено <b>%s</b> р. остатка с предыдущего месяца. Все траты перемещены в архив. %s'

    def counting_additional_list(self, diff):

        danger_info = False

        categories = self.configuration.category.all()
        count_category = categories.count()
        distribution = diff / count_category
        if distribution == int(distribution):
            list_values_add = [distribution] * count_category
        else:
            list_values_add = [floor(distribution)] * count_category
            list_values_add[-1] += diff - (floor(distribution) * count_category)

        # Проверка на отрицательное значение в лимите категорий
        for n, cat in enumerate(categories):
            if cat.max + list_values_add[n] <= 0:
                danger_info = True

                # Так как при перерасчете лимитов у нас вышло отрицательное число, рассчитываем лимиты по ровну и
                # предупреждаем об этом пользователя
                income = self.configuration.income
                distribution = income / count_category
                if distribution == int(distribution):
                    list_values_add = [distribution] * count_category
                else:
                    list_values_add = [floor(distribution)] * count_category
                    list_values_add[-1] += diff - (floor(distribution) * count_category)
                break

        return list_values_add, danger_info

    def post(self, *args, **kwargs):

        status = balance = 0

        # Наша конфигурация
        configuration = self.configuration

        # Проверочные данные для избежания ошибок
        categoryes = configuration.category.all()
        input_income = int(self.POST('number'))

        # Берем деньги с общего счета
        self.take_money(input_income)

        if input_income >= len(categoryes):

            # Значения configuration перед обновлением
            last_income = configuration.income
            last_date = configuration.date
            # Рассчитываем непотраченный остаток с предыдущего месяца
            balance = last_income - sum(
                list(map(lambda x: x.value, Cost.objects.filter(costcategory__configuration=configuration))))
            # Вносим новые правки в план
            configuration.income = input_income
            configuration.date = datetime.now().date()
            configuration.save()
            # Непотраченный остаток присваиваем к общему счету
            self.add_money(balance)
            # Получаем добавочный список
            list_values_add, danger_info = self.counting_additional_list((input_income - last_income))
            # Создаем таблицу архива
            archive = Archive(date_one=last_date)
            archive.save()

            # Переменная суммы трат
            amount_cost = 0

            for n, category in enumerate(categoryes):
                costs = category.cost.all()
                # Перемещаем данные в архив
                archive.archive_costs.add(*[cost for cost in costs])
                # Считаем сумму трат
                amount_cost += sum([cost.value for cost in costs])
                category.cost.clear()
                cat = category
                # Корректируем лимиты категорий
                if not danger_info:
                    cat.max += list_values_add[n]
                else:
                    cat.max = list_values_add[n]
                cat.save()

            # Записываем сумму трат, сыкономленную и общую
            archive.spent = amount_cost
            archive.saved = last_income - amount_cost
            archive.income = last_income
            archive.save()

            # Прикрепляем полученный архив в нашей конфгурации
            configuration.archive.add(archive)

            comment = self.POST('comment') if self.POST('comment') else ''

            self.action_dispatch(description=self.description_for_action_record % (balance, comment),
                                 settings=self.request.user.settings, configuration=configuration)

            status = 1 if not danger_info else 2

        response = {'status': status, 'balance': balance}
        return HttpResponse(json.dumps(response), content_type='application/json')


class InputMiddleIncomePlan(StartNewPeriod):

    description_for_action_record = 'Добавлены деньги к плану сумму <b>%s</b> р. %s'

    def post(self, *args, **kwargs):
        status = 0
        middle_income = int(self.POST('number'))
        configuration = self.configuration

        self.take_money(middle_income)

        categoryes = configuration.category.all()
        if middle_income >= len(categoryes):

            configuration.income += middle_income
            configuration.save()

            list_values_add = self.counting_additional_list(middle_income)[0]

            for n, category in enumerate(categoryes):
                _category = category
                _category.max += list_values_add[n]
                _category.save()

            status = 1

            comment = self.POST('comment') if self.POST('comment') else ''

            self.action_dispatch(description=self.description_for_action_record % (str(middle_income), comment),
                                 settings=self.request.user.settings, configuration=self.configuration)

        return HttpResponse(json.dumps({'status': status}), content_type='application/json')


class DeletePlan(ActionsView):

    description_for_action_record = 'План <b>%s</b> был удалён.'

    def post(self, *args, **kwargs):
        balance = self.configuration.income - sum(
            list(map(lambda x: x.value, Cost.objects.filter(costcategory__configuration=self.configuration))))

        # Данные для записи в историю
        name = self.configuration.name

        self.add_money(balance)

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

        print(self.request.POST)

        current_category = configuration.category.all()
        number_category = 0
        c = [item[1] for item in self.request.POST.items()][5:]

        # Удаляем лишние категории, если есть
        for extra_category in configuration.category.all()[len(c)//2:len(current_category)]:
            extra_category.delete()

        for n, item in enumerate(c):
            if n % 2 == 1 and c[n - 1] and c[n]:

                # Делаем изменения в категориях. Если есть новая, то по ошибке направляемся её создавать
                try:
                    if not (current_category[number_category].name == c[n - 1] and
                            current_category[number_category].max == c[n]):
                        for_save = current_category[number_category]
                        for_save.name = c[n - 1]
                        for_save.max = c[n]
                        for_save.save()
                except IndexError:
                    new_category = CostCategory(name=c[n - 1], max=c[n])
                    new_category.save()
                    configuration.category.add(new_category)
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


class CreateShoppingList(ActionsView):

    def post(self, *args, **kwargs):

        # Либо существующий список, либо созданный
        if self.request.POST.get('id'):
            shopping_list = ShoppingList.objects.get(id=self.POST('id'))
        else:
            shopping_list = ShoppingList()
            shopping_list.save()

        # Добавляем новый элемент, или обрабатываем существующие
        if self.request.POST.getlist('new-item'):
            shopping_list_item = ShoppingListItem(name='', count=1, price=0)
            shopping_list_item.save()
            shopping_list.item.add(shopping_list_item)
        else:
            shopping_list.name = self.POST('name-list')
            shopping_list.save()
            self.configuration.shopping_list.add(shopping_list)

            if self.request.POST.get('id-item'):
                ids_items = self.request.POST.getlist('id-item')
                name_item = self.request.POST.getlist('name-item')
                count_item = self.request.POST.getlist('count')
                price_item = self.request.POST.getlist('price')
                category_item = self.request.POST.getlist('item-category')
                flag_item = self.request.POST.getlist('flag')
                for n, id in enumerate(ids_items):
                    item = ShoppingListItem.objects.get(id=id)
                    item.name = name_item[n]
                    if count_item[n]:
                        item.count = count_item[n]
                    if category_item[n]:
                        item.category_id = int(category_item[n])
                    if price_item[n]:
                        item.price = price_item[n]
                    item.flag = bool(int(flag_item[n]))
                    item.save()

        return HttpResponse(json.dumps({'id': shopping_list.id}), content_type='application/json')


class InputCostShoppingList(ActionsView):

    description_for_action_record = 'Зафиксирован расход на сумму <b>%s</b> <i class="fa fa-rub" aria-hidden="true"></i>'

    def post(self, *args, **kwargs):
        # Счетчик суммы всех трат для записи в action_record
        n = 0
        # Получаемый требуемый шоп-лист
        shopping_list = ShoppingList.objects.get(id=kwargs['id'])
        # Начинаем перебирать весь список
        for item in shopping_list.item.all():
            # Если позиция отмечена
            if item.flag:
                # Получаем нужную категорию траты
                category = item.category
                # Добавляем столько трат, сколько указано количество товара
                for i in list(range(item.count)):
                    # Считаем сумму
                    n += item.price
                    # Создаем трату
                    cost = Cost(value=item.price, detailed_comment=item.name)
                    cost.save()
                    # Получаем нужную метку
                    tag_obj, b = Tags.objects.update_or_create(user=str(self.request.user), name=shopping_list.name)
                    # Добавляем к трате метку
                    cost.tags.add(tag_obj)
                    # Записываем трату в категорию
                    category.cost.add(cost)

        self.action_dispatch(description=self.description_for_action_record % n,
                             settings=self.request.user.settings, configuration=self.configuration)

        return HttpResponse('ok')


class DeleteItem(ActionsView):
    model = None

    def post(self, *args, **kwargs):
        self.model.objects.get(id=kwargs['id']).delete()
        return HttpResponse('ok')
