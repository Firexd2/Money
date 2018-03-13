from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from Core.models import CostCategory, Cost, Tags, Archive


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
    def tags_info(self):
        tags = Tags.objects.filter(user=self.request.user)
        income = self.configuration.income
        info_list = []
        for tag in tags:
            number = sum(map(lambda x: x.value, self.list_costs.filter(tags=tag.id)))
            info_list.append((tag.name, number, str(number / income * 100)))
        return sorted(info_list, key=lambda x: x[1], reverse=True)

    def get_context_data(self, **kwargs):
        context = super(StatTemplatePlanView, self).get_context_data(**kwargs)
        context['costs'] = self.list_costs
        context['max_cost'] = max(context['costs'], key=lambda x: x.value, default=0)
        context['middle_cost'] = round(sum([cost.value for cost in context['costs']]) /
                            ((datetime.now().date() - self.configuration.date).days + 1))
        context['middle_cost_of_week'] = context['middle_cost'] * 8
        context['days'] = (datetime.today().date() - self.configuration.date).days
        context['now_week'] = context['days'] // 8
        context['number_days_for_week'] = (context['days'] // 8 + 1) * 8 - context['days']
        context['tags'] = self.tags_info
        return context


class CostTemplatePlanView(BaseTemplatePlanView):
    def get_context_data(self, **kwargs):
        context = super(CostTemplatePlanView, self).get_context_data(**kwargs)
        context['costs'] = Cost.objects.filter(costcategory__configuration=self.configuration)\
            .order_by('-datetime')
        context['tags'] = Tags.objects.filter(user=str(self.request.user)).order_by('-datetime')[:10]
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

        spent = middle_cost = days = 0
        biggest_cost = [0, '']
        dict_tags = dict()

        archives = Archive.objects.filter(configuration=self.configuration)
        archive_costs = Cost.objects.filter(archive__in=[archive.id for archive in archives]).filter(datetime__lte=date_two, datetime__gte=date_one)[::-1]

        # Считаем количество дней между первым и последним днем выбранного периода
        days = (date_two - date_one).days
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

        return {'spent': spent, 'middle_cost': middle_cost,
                'biggest_cost': biggest_cost, 'dict_tags': sorted(dict_tags.items(), key=lambda x: x[1], reverse=True),
                'costs': archive_costs, 'days': days}

    def get_context_data(self, **kwargs):
        context = super(ArchiveReportLastPeriodView, self).get_context_data(**kwargs)
        result_report = self.report_last_period(**kwargs)
        for key in result_report:
            context[key] = result_report[key]
        return context


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
