import json
from datetime import datetime
from math import floor
from django.http import HttpResponse
from django.views.generic.base import View

from Core.models import Configuration, CostCategory, Cost, Tags


class ActionsView(View):
    @classmethod
    def configuration(cls, request):
        return request.user.settings.configurations.all().get(name_url=request.POST['name'])


class CorrectFreeMoney(ActionsView):
    def post(self, *args, **kwargs):
        settings = self.request.user.settings
        settings.free_money = self.request.POST['value']
        settings.save()
        return HttpResponse('ok')


class CreateNewPlan(ActionsView):
    def post(self, *args, **kwargs):
        configuration = Configuration(name=self.request.POST['name-plan'], income=self.request.POST['income'],
                                      icon=self.request.POST['icon'], color=self.request.POST['color'])
        configuration.save()
        c = [item[1] for item in self.request.POST.items()][4:]
        for n, item in enumerate(c):
            if n % 2 == 1 and c[n - 1] and c[n]:
                cost_category = CostCategory(name=c[n - 1], max=c[n])
                cost_category.save()
                configuration.category.add(cost_category)
        self.request.user.settings.configurations.add(configuration)

        return HttpResponse('ok')


class StartNewPeriod(ActionsView):
    def post(self, *args, **kwargs):
        # Наша конфигурация
        configuration = self.configuration(self.request)
        # Предыдущее значение income
        last_income = configuration.income
        # Рассчитываем непотраченный остаток с предыдущего месяца
        balance = last_income - sum(
            list(map(lambda x: x.value, Cost.objects.filter(costcategory__configuration=configuration))))
        # Вносим новые правки в план
        configuration.income = int(self.request.POST['income'])
        configuration.date = datetime.now().date()
        configuration.save()
        # Непотраченный остаток присваиваем к общему счету
        settings = configuration.settings_set.all()[0]
        settings.free_money += balance
        settings.save()
        # Удаляем траты и производим перерасчет максимумов в категориях на основе введенных данных
        count_category = configuration.category.all().count()
        distribution = (int(self.request.POST['income']) - last_income) / count_category
        if distribution == int(distribution):
            list_values_add = [distribution] * count_category
        else:
            list_values_add = [floor(distribution)] * count_category
            list_values_add[-1] += int(self.request.POST['income']) - last_income - (floor(distribution) * count_category)
        for n, category in enumerate(configuration.category.all()):
            category.cost.all().delete()
            cat = category
            cat.max += list_values_add[n]
            cat.save()
        response = {'status': 1, 'balance': balance}
        return HttpResponse(json.dumps(response), content_type='application/json')


class EditDate(ActionsView):
    def post(self, *args, **kwargs):
        date = datetime.strptime(self.request.POST['date'], '%Y-%m-%d').date()
        status = 0
        if datetime.now().date() >= date:
            self.configuration(self.request).date = date
            self.configuration(self.request).save()
            status = 1
        response = {'status': status}

        return HttpResponse(json.dumps(response), content_type='application/json')


class DeletePlan(ActionsView):
    def post(self, *args, **kwargs):
        balance = self.configuration(self.request).income - sum(
            list(map(lambda x: x.value, Cost.objects.filter(costcategory__configuration=self.configuration(self.request)))))
        settings = self.configuration(self.request).settings_set.all()[0]
        settings.free_money += balance
        settings.save()
        try:
            self.configuration(self.request).delete()
            status = 1
        except:
            status = 0
        response = {'status': status}

        return HttpResponse(json.dumps(response), content_type='application/json')


class SettingsPlan(ActionsView):
    def post(self, *args, **kwargs):
        self.configuration(self.request).name = self.request.POST['name-plan']
        self.configuration(self.request).income = self.request.POST['income']
        self.configuration(self.request).icon = self.request.POST['icon']
        self.configuration(self.request).color = self.request.POST['color']
        self.configuration(self.request).save()

        current_category = self.configuration(self.request).category.all()
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

        return HttpResponse('ok')


class ToggleCategoryWeekTable(ActionsView):
    def post(self, *args, **kwargs):
        bool_field = self.configuration(self.request).category.all().get(name=self.request.POST['category'])
        bool_field.included_week_table = not bool_field.included_week_table
        bool_field.save()
        return HttpResponse('ok')


class InputCost(ActionsView):
    def post(self, *args, **kwargs):
        for cat in self.configuration(self.request).category.all():
            value = 'value-' + str(cat.id)
            detailed_comment = 'detail-comment-' + str(cat.id)
            n = 0
            while True:
                complete_value = value + '-' + str(n)
                complete_detailed_comment = detailed_comment + '-' + str(n)
                try:
                    cost = Cost(value=self.request.POST[complete_value],
                                detailed_comment=self.request.POST[complete_detailed_comment])
                except KeyError:
                    break
                cost.save()

                for tag in self.request.POST.getlist('tags'):
                    tag_obj, b = Tags.objects.update_or_create(user=str(self.request.user), name=tag)
                    cost.tags.add(tag_obj)
                cat.cost.add(cost)
                n += 1

        return HttpResponse('ok')


class DeleteCost(ActionsView):
    def post(self, *args, **kwargs):
        Cost.objects.filter(costcategory__configuration=self.configuration(self.request)) \
            .order_by('-datetime').get(id=self.request.POST['id']).delete()
        return HttpResponse('ok')



def archiving(name, *args):

    pass
