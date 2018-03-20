import json
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, DetailView
from Core.models import CostCategory, Cost, Tags, Archive, ShoppingList


@method_decorator(login_required, name='dispatch')
class BaseTemplatePlanView(TemplateView):

    @property
    def configuration(self):
        return self.request.user.settings.configurations.all().get(name_url=self.kwargs['name_url'])

    @property
    def list_costs(self):
        return Cost.objects.filter(costcategory__configuration=self.configuration).order_by('-datetime')

    def get_context_data(self, **kwargs):
        context = super(BaseTemplatePlanView, self).get_context_data(**kwargs)
        context['configuration'] = self.configuration
        context['history'] = self.configuration.history.all()[::-1]
        return context


class StatTemplatePlanView(BaseTemplatePlanView):

    @property
    def get_tags_info(self):
        tags = Tags.objects.filter(user=self.request.user)
        income = self.configuration.income
        info_list = []
        for tag in tags:
            number = sum(map(lambda x: x.value, self.list_costs.filter(tags=tag.id)))
            info_list.append((tag.name, number, str(number / income * 100)))
        return sorted(info_list, key=lambda x: x[1], reverse=True)

    @property
    def get_days_info(self):
        days = []
        income = self.configuration.income
        # Необходимая мера для начальной точки
        day_one = self.configuration.date - timedelta(days=1)
        day_two = datetime.now().date()
        for delta_day in list(range((day_two - day_one).days + 1)):
            day = (day_one + timedelta(days=delta_day))
            days.append((day.strftime('%Y-%m-%d'),
                         income - sum([cost.value for cost in self.list_costs if cost.datetime.date() <= day])))
        return days

    @property
    def stat(self):
        costs = self.list_costs
        max_cost = max(costs, key=lambda x: x.value, default=0)
        middle_cost = round(sum([cost.value for cost in costs]) /
                            ((datetime.now().date() - self.configuration.date).days + 1))
        middle_cost_of_week = middle_cost * 8
        days = (datetime.today().date() - self.configuration.date).days
        now_week = days // 8
        number_days_for_week = (days // 8 + 1) * 8 - days
        tags = self.get_tags_info
        days_info = self.get_days_info
        return locals()

    def get_context_data(self, **kwargs):
        context = super(StatTemplatePlanView, self).get_context_data(**kwargs)
        stat = self.stat
        for key in stat:
            if key not in ['self']:
                context[key] = stat[key]
        return context


class CostTemplatePlanView(BaseTemplatePlanView):
    def get_context_data(self, **kwargs):
        context = super(CostTemplatePlanView, self).get_context_data(**kwargs)
        context['costs'] = Cost.objects.filter(costcategory__configuration=self.configuration)\
            .order_by('-datetime')
        context['tags'] = Tags.objects.filter(user=str(self.request.user)).order_by('-datetime')[:10]
        return context


class ShoppingListTemplateView(BaseTemplatePlanView):
    def get_context_data(self, **kwargs):
        context = super(ShoppingListTemplateView, self).get_context_data(**kwargs)
        context['shopping_lists'] = ShoppingList.objects.filter(configuration=self.configuration)[::-1]
        return context


class DetailShoppingListTemplateView(BaseTemplatePlanView):
    def get_context_data(self, **kwargs):
        context = super(DetailShoppingListTemplateView, self).get_context_data(**kwargs)
        if int(kwargs['id']):
            context['list'] = ShoppingList.objects.get(id=int(kwargs['id']))
        return context


class ArchiveTemplatePlanView(BaseTemplatePlanView):

    def get_context_data(self, **kwargs):
        context = super(ArchiveTemplatePlanView, self).get_context_data(**kwargs)
        context['archive'] = Archive.objects.filter(configuration=self.configuration)[::-1]
        return context


class ArchiveReportLastPeriodView(BaseTemplatePlanView):

    def report_last_period(self, **kwargs):

        date_one = datetime.strptime(kwargs['date_one'], '%Y-%m-%d')
        date_two = datetime.strptime(kwargs['date_two'], '%Y-%m-%d')

        spent = 0
        biggest_cost = [0, '']
        dict_tags = dict()

        archives = Archive.objects.filter(configuration=self.configuration)
        archive_costs = Cost.objects.filter(archive__in=
                                            [archive.id for archive in archives]).filter(datetime__lte=
                                                      date_two + timedelta(days=1), datetime__gte=date_one).order_by('-datetime')

        # Считаем количество дней между первым и последним днем выбранного периода
        days = (date_two - date_one).days + 1
        for cost in archive_costs:
            # Считаем, сколько потрачено за выбранный период
            spent += cost.value
            # Находим самую большу трату
            if biggest_cost[0] < cost.value:
                biggest_cost[0] = cost.value
                biggest_cost[1] = cost.detailed_comment
            # Формируем словарь из тегов и их обших сумм
            for tag in cost.tags.all():
                if dict_tags.get(tag.name):
                    dict_tags[tag.name] += cost.value
                else:
                    dict_tags[tag.name] = cost.value
        # Получаем значение средней траты за день
        middle_cost = round(spent / days)

        dict_tags = sorted(dict_tags.items(), key=lambda x: x[1], reverse=True)

        return locals()

    def get_context_data(self, **kwargs):
        context = super(ArchiveReportLastPeriodView, self).get_context_data(**kwargs)
        result_report = self.report_last_period(**kwargs)
        for key in result_report:
            if key not in ('date_one', 'date_two', 'self', 'kwargs'):
                context[key] = result_report[key]
        return context


class GetDatesInArchive(BaseTemplatePlanView):

    def post(self, *args, **kwargs):

        request = kwargs['type_date'].split('-')
        if request[0] == 'time':
            date_now = datetime.now()
            if request[1].isdigit():
                date_one = (date_now - timedelta(days=int(request[1])*30)).date()
            else:
                date_one = self.request.user.date
            date_two = date_now.date()
        else:
            archives = Archive.objects.filter(configuration=self.configuration)[::-1][:int(request[1])]
            date_one = archives[-1].date_one
            date_two = archives[0].date_two

        return HttpResponse(json.dumps({'date_one': date_one.strftime('%Y-%m-%d'),
                                        'date_two': date_two.strftime('%Y-%m-%d')}), content_type='application/json')


class TagDetailView(BaseTemplatePlanView):
    def get_context_data(self, **kwargs):
        context = super(TagDetailView, self).get_context_data(**kwargs)
        tag = Tags.objects.get(name=kwargs['name'])
        context['cost'] = self.list_costs.filter(tags=tag)
        return context


@method_decorator(login_required, name='dispatch')
class BaseTemplateView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(BaseTemplateView, self).get_context_data(**kwargs)
        context['money_circulation'] = sum([conf.income for conf in self.request.user.settings.configurations.all()])
        context['history'] = self.request.user.settings.history.all()[::-1]
        return context


class CategoryDetailView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context['category'] = CostCategory.objects.get(id=kwargs['id'])
        return context


class TableInputCostShoppingList(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(TableInputCostShoppingList, self).get_context_data(**kwargs)
        context['shop_list'] = ShoppingList.objects.get(id=kwargs['id'])
        return context