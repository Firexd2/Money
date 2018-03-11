from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from Core.models import CostCategory, Cost, Tags


@method_decorator(login_required, name='dispatch')
class BaseTemplatePlanView(TemplateView):

    @property
    def configuration(self):
        return self.request.user.settings.configurations.all().get(name_url=self.kwargs['name_url'])

    def get_context_data(self, **kwargs):
        context = super(BaseTemplatePlanView, self).get_context_data(**kwargs)
        context['configuration'] = self.configuration
        context['history'] = self.configuration.history.all()[::-1]
        return context


class StatTemplatePlanView(BaseTemplatePlanView):

    @property
    def tags_info(self):
        tags = Tags.objects.filter(user=self.request.user)
        info_list = []
        for tag in tags:
            info_list.append((tag.name, sum(map(lambda x: x.value, self.list_costs.filter(tags=tag.id)))))
        return sorted(info_list, key=lambda x: x[1], reverse=True)

    @property
    def list_costs(self):
        return Cost.objects.filter(costcategory__configuration=self.configuration).order_by('-datetime')

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
