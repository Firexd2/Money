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
        return context


class StatTemplatePlanView(BaseTemplatePlanView):

    def get_context_data(self, **kwargs):
        context = super(StatTemplatePlanView, self).get_context_data(**kwargs)
        context['costs'] = Cost.objects.filter(costcategory__configuration=context['configuration'])\
            .order_by('-datetime')
        context['max_cost'] = max(context['costs'], key=lambda x: x.value, default=0)
        middle_cost = round(sum([cost.value for cost in context['costs']]) /
                            ((datetime.now().date() - context['configuration'].date).days + 1))
        context['middle_cost_of_week'] = middle_cost * 8
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
        return context


class CategoryDetailView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context['category'] = CostCategory.objects.get(id=kwargs['id'])
        return context


# @login_required
# def panel(request):
#     money_circulation = sum([conf.income for conf in request.user.settings.configurations.all()])
#     return render(request, 'panel/panel.html', locals())


# @login_required
# def new(request):
#     return render(request, 'panel/new.html', locals())


# def home_plan(request, name_url):
#     configuration = request.user.settings.configurations.all().get(name_url=name_url)
#     return render(request, 'plan/home.html', locals())


# def settings(request, name_url):
#     configuration = request.user.settings.configurations.all().get(name_url=name_url)
#     return render(request, 'plan/settings.html', locals())


# def category_detail(request, id):
#     category = CostCategory.objects.get(id=id)
#     return render(request, 'plan/category_detail.html', locals())


# def stat(request, name_url):
#
#     configuration = request.user.settings.configurations.get(name_url=name_url)
#     costs = Cost.objects.filter(costcategory__configuration=configuration).order_by('-datetime')
#     max_cost = max(costs, key=lambda x: x.value, default=0)
#     middle_cost = round(sum([cost.value for cost in costs]) / ((datetime.now().date() - configuration.date).days + 1))
#     middle_cost_of_week = middle_cost * 8
#
#     days = (datetime.today().date() - configuration.date).days
#     now_week = days // 8
#     number_days_for_week = (days // 8 + 1) * 8 - days
#
#     return render(request, 'plan/stat.html', locals())


# def cost(request, name_url):
#     configuration = request.user.settings.configurations.all().get(name_url=name_url)
#     costs = Cost.objects.filter(costcategory__configuration=configuration).order_by('-datetime')
#     tags = Tags.objects.filter(user=str(request.user)).order_by('-datetime')[:10]
#
#     return render(request, 'plan/cost.html', locals())
