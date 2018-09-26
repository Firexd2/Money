import json
from datetime import datetime
from math import floor

from django.http import HttpResponse
from django.utils.encoding import uri_to_iri
from django.views.generic.base import View

from Core.models import Archive, Configuration, Cost, CostCategory, History, ShoppingList, ShoppingListItem, Tags, \
    VersionControl


class ActionsView(View):

    @staticmethod
    def description_for_action_record(name):
        descriptions = {
            'AddIncome': 'Добавлен доход на сумму <b>%s</b> <i class="fa fa-rub" aria-hidden="true"></i>.'
                         ' Комментарий: <b>%s</b>',

            'TakeIncome': 'Со счета неиспользованных денег было изъято <b>%s</b> '
                          '<i class="fa fa-rub" aria-hidden="true"></i>. Комментарий: <b>%s</b>',

            'CreateNewPlan': 'Создан новый план распределения бюджета <b style="color:%s">'
                             '<i class="%s" aria-hidden="true"></i> %s</b>.',

            'StartNewPeriod': 'Начало нового рассчетного периода. На счет неиспользованных денег'
                              ' было зачислено <b>%s</b> <i class="fa fa-rub" aria-hidden="true"></i> остатка'
                              ' с предыдущего периода. Все траты перемещены в архив. %s',

            'InputMiddleIncomePlan': 'Добавлены дополнительные средства в план - '
                                     '<b>%s</b> <i class="fa fa-rub" aria-hidden="true"></i>. %s',

            'DeletePlan': 'План <b>%s</b> был удалён.',

            'SettingsPlan': 'Отредактирован план',

            'InputCost': 'Зафиксирован расход на сумму <b>%s</b> <i class="fa fa-rub" aria-hidden="true"></i>',

            'DeleteCost': 'Удалена трата на сумму <b>%s</b> <i class="fa fa-rub"'
                          ' aria-hidden="true"></i> с комментарием: %s',

            'InputCostShoppingList': 'Зафиксирован расход на сумму <b>%s</b>'
                                     ' <i class="fa fa-rub" aria-hidden="true"></i>',

            'ChangeTags': 'Была успешно произведена миграция трат с метки "<b>%s</b>" на метку "<b>%s</b>".'
                          ' Изменено <b>%s</b> шт. трат.'

        }

        return descriptions[name]

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
        return self.request.user.settings.configurations.all().get(name=uri_to_iri(self.request.POST['name']))

    @staticmethod
    def action_dispatch(**kwargs):

        if len(kwargs) == 3:
            history_for_settings = History(description='<b>' + kwargs['configuration'].name
                                                       + '</b>: ' + kwargs['description'])
            history_for_settings.save()

            history_for_configuration = History(description=kwargs['description'])
            history_for_configuration.save()

            kwargs['settings'].history.add(history_for_settings)
            kwargs['configuration'].history.add(history_for_configuration)
        else:
            history = History(description=kwargs['description'])
            history.save()
            kwargs['settings'].history.add(history)


class AddIncome(ActionsView):

    def post(self, *args, **kwargs):
        self.add_money(self.POST('number'))

        description = self.description_for_action_record(self.__class__.__name__) %\
                      (self.POST('number'), self.POST('comment'))

        self.action_dispatch(description=description, settings=self.request.user.settings)
        return HttpResponse('ok')


class TakeIncome(ActionsView):

    def post(self, *args, **kwargs):
        self.take_money(self.POST('number'))

        description = self.description_for_action_record(self.__class__.__name__) %\
                      (self.POST('number'), self.POST('comment'))

        self.action_dispatch(description=description, settings=self.request.user.settings)
        return HttpResponse('ok')


class CreateNewPlan(ActionsView):

    def post(self, *args, **kwargs):

        self.take_money(int(self.POST('income')))

        configuration = Configuration(name=self.POST('name-plan'), income=self.POST('income'),
                                      icon=self.POST('icon'), color=self.POST('color'))
        configuration.save()

        names_cat = self.request.POST.getlist('name-cat')
        limits_cat = self.request.POST.getlist('limit')

        for n, name in enumerate(names_cat):
            cost_category = CostCategory(name=name, max=limits_cat[n])
            cost_category.save()
            configuration.category.add(cost_category)

        self.request.user.settings.configurations.add(configuration)

        description = self.description_for_action_record(self.__class__.__name__) %\
                      (configuration.color, configuration.icon, configuration.name)

        self.action_dispatch(description=description, settings=self.request.user.settings)

        return HttpResponse('ok')


class StartNewPeriod(ActionsView):

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
                list(map(lambda x: x.value, Cost.objects.filter(category__configuration=configuration))))
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

            description = self.description_for_action_record(self.__class__.__name__) % (balance, comment)

            self.action_dispatch(description=description,
                                 settings=self.request.user.settings, configuration=configuration)

            status = 1 if not danger_info else 2

        response = {'status': status, 'balance': balance}
        return HttpResponse(json.dumps(response), content_type='application/json')


class InputMiddleIncomePlan(StartNewPeriod):

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

            description = self.description_for_action_record(self.__class__.__name__) % (str(middle_income), comment)

            self.action_dispatch(description=description,
                                 settings=self.request.user.settings, configuration=self.configuration)

        return HttpResponse(json.dumps({'status': status}), content_type='application/json')


class DeletePlan(ActionsView):

    def post(self, *args, **kwargs):
        balance = self.configuration.income - sum(
            list(map(lambda x: x.value, Cost.objects.filter(category__configuration=self.configuration))))

        # Данные для записи в историю
        name = self.configuration.name

        self.add_money(balance)

        self.action_dispatch(description=self.description_for_action_record(self.__class__.__name__) % name,
                             settings=self.request.user.settings)
        try:
            self.configuration.delete()
            status = 1
        except:
            status = 0
        response = {'status': status}

        return HttpResponse(json.dumps(response), content_type='application/json')


class SettingsPlan(ActionsView):

    def post(self, *args, **kwargs):

        configuration = self.configuration
        configuration.name = self.POST('name-plan')
        configuration.income = self.POST('income')
        configuration.icon = self.POST('icon')
        configuration.color = self.POST('color')
        configuration.save()

        for item_category in configuration.category.all():
            category = item_category
            try:
                category.name = self.POST('name' + str(category.id))
                category.max = self.POST('limit' + str(category.id))
                category.save()
            except KeyError:
                category.delete()

        new_category_names = self.request.POST.getlist('name-cat')
        new_category_limits = self.request.POST.getlist('limit')

        if new_category_limits:
            for n, name in enumerate(new_category_names):
                cost_category = CostCategory(name=name, max=new_category_limits[n])
                cost_category.save()
                configuration.category.add(cost_category)

        self.action_dispatch(description=self.description_for_action_record(self.__class__.__name__),
                             settings=self.request.user.settings, configuration=configuration)

        return HttpResponse('ok')


class ToggleCategoryWeekTable(ActionsView):
    def post(self, *args, **kwargs):
        bool_field = self.configuration.category.all().get(name=self.POST('category'))
        bool_field.included_week_table = not bool_field.included_week_table
        bool_field.save()
        return HttpResponse('ok')


class InputCost(ActionsView):

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

        self.action_dispatch(description=self.description_for_action_record(self.__class__.__name__) % number,
                             settings=self.request.user.settings, configuration=self.configuration)

        return HttpResponse('ok')


class DeleteCost(ActionsView):

    def post(self, *args, **kwargs):
        cost = Cost.objects.filter(category__configuration=self.configuration).get(id=self.POST('id'))
        value = cost.value
        comment = cost.detailed_comment
        cost.delete()

        self.action_dispatch(description=self.description_for_action_record(self.__class__.__name__) % (value, comment),
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

        self.action_dispatch(description=self.description_for_action_record(self.__class__.__name__) % n,
                             settings=self.request.user.settings, configuration=self.configuration)

        return HttpResponse('ok')


class DeleteItem(ActionsView):
    model = None

    def post(self, *args, **kwargs):
        self.model.objects.get(id=kwargs['id']).delete()
        return HttpResponse('ok')


class ChangeTags(ActionsView):

    def change_tags_in_costs(self, src_tag,  dst_tag, update_current_plan, update_archive):

        # счетчики измененых трат
        count_cost_in_current_plan = 0
        count_cost_in_archive = 0

        if update_current_plan:
            # получаем все текущие траты с нужной меткой
            all_cost = Cost.objects.filter(category__configuration=self.configuration, tags=src_tag)
            for cost in all_cost:
                cost.tags.remove(src_tag)
                cost.tags.add(dst_tag)
                count_cost_in_current_plan += 1

        if update_archive:
            # получаем все архивы нашего плана
            all_acrchives = self.configuration.archive.all()
            for archive in all_acrchives:
                all_cost = archive.archive_costs.filter(tags=src_tag)
                for cost in all_cost:
                    cost.tags.remove(src_tag)
                    cost.tags.add(dst_tag)
                    count_cost_in_archive += 1

        return {'current_plan': count_cost_in_current_plan,
                'archives': count_cost_in_archive}

    def post(self, *args, **kwargs):

        src_tag_name = self.request.POST.get('src-tag')
        dst_tag_name = self.request.POST.get('dst-tag')
        current_costs = self.request.POST.get('current-costs')
        archive_costs = self.request.POST.get('archive-costs')
        delete_src_tag = self.request.POST.get('delete-src-tag')

        if src_tag_name == dst_tag_name or (not current_costs and not archive_costs):

            if src_tag_name == dst_tag_name:
                info = 'Тэги должны быть разными.'
            else:
                info = 'Вы не выбрали, где нужно произвести замену трат.'

            return HttpResponse(json.dumps({'status': 0, 'info': info}), content_type='application/json')

        try:
            src_tag = Tags.objects.get(name=src_tag_name, user=self.request.user.username)
        except Tags.DoesNotExist:
            info = 'Первой метки не существует.'
            return HttpResponse(json.dumps({'status': 0, 'info': info}), content_type='application/json')

        try:
            dst_tag = Tags.objects.get(name=dst_tag_name, user=self.request.user.username)
        except Tags.DoesNotExist:
            dst_tag = Tags.objects.create(name=dst_tag_name, user=self.request.user.username)

        result = self.change_tags_in_costs(src_tag, dst_tag, current_costs, archive_costs)

        if delete_src_tag and not Cost.objects.filter(tags=src_tag).exists():
            src_tag.delete()

        response = {'status': 1}
        response.update(result)

        self.action_dispatch(description=self.description_for_action_record(self.__class__.__name__)
                                         % (src_tag_name, dst_tag_name, sum(result.values())),
                             settings=self.request.user.settings,
                             configuration=self.configuration)

        return HttpResponse(json.dumps(response), content_type='application/json')


def first_log_in_trigger(request):
    user = request.user
    user.first_log_in = False
    user.save()
    return HttpResponse('ok')


def look_last_version(request):
    user = request.user
    user.look_version_id = VersionControl.objects.all().last().id
    user.save()
    return HttpResponse('ok')
