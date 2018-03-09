from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from Core.models import CostCategory, Cost, Tags


@method_decorator(login_required, name='dispatch')
class BaseTemplatePlanView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(BaseTemplatePlanView, self).get_context_data(**kwargs)
        context['configuration'] = self.request.user.settings.configurations.all().get(name_url=self.kwargs['name_url'])
        context['history'] = context['configuration'].history.all()[::-1]
        return context


class StatTemplatePlanView(BaseTemplatePlanView):
    def get_context_data(self, **kwargs):
        context = super(StatTemplatePlanView, self).get_context_data(**kwargs)
        context['costs'] = Cost.objects.filter(costcategory__configuration=context['configuration'])\
            .order_by('-datetime')
        context['max_cost'] = max(context['costs'], key=lambda x: x.value, default=0)
        context['middle_cost'] = round(sum([cost.value for cost in context['costs']]) /
                            ((datetime.now().date() - context['configuration'].date).days + 1))
        context['middle_cost_of_week'] = context['middle_cost'] * 8
        context['days'] = (datetime.today().date() - context['configuration'].date).days
        context['now_week'] = context['days'] // 8
        context['number_days_for_week'] = (context['days'] // 8 + 1) * 8 - context['days']
        return context


class CostTemplatePlanView(BaseTemplatePlanView):
    def get_context_data(self, **kwargs):
        context = super(CostTemplatePlanView, self).get_context_data(**kwargs)
        context['costs'] = Cost.objects.filter(costcategory__configuration=context['configuration'])\
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
