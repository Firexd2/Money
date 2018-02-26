from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from Core.models import Configuration, CostCategory, Cost, Tags


@csrf_exempt
@login_required
def panel(request):

    money_circulation = sum([conf.income for conf in request.user.settings.configurations.all()])

    if request.is_ajax():
        settings = request.user.settings
        settings.free_money = request.POST['value']
        settings.save()

    return render(request, 'panel.html', locals())


@login_required
def new(request):
    if request.POST:
        configuration = Configuration(name=request.POST['name'], income=request.POST['income'],
                                      icon=request.POST['icon'], color=request.POST['color'])
        configuration.save()
        c = [item[1] for item in request.POST.items()][5:]
        for n, item in enumerate(c):
            if n % 2 == 1 and c[n - 1] and c[n]:
                cost_category = CostCategory(name=c[n - 1], max=c[n])
                cost_category.save()
                configuration.category.add(cost_category)
        request.user.settings.configurations.add(configuration)
        return redirect('panel')
    return render(request, 'new.html', locals())


def conf(request, name_url):

    configuration = request.user.settings.configurations.all().get(name_url=name_url)

    if request.POST:
        configuration.name = request.POST['name']
        configuration.income = request.POST['income']
        configuration.icon = request.POST['icon']
        configuration.color = request.POST['color']
        configuration.save()

    current_category = configuration.category.all()
    number_category = 0
    c = [item[1] for item in request.POST.items()][5:]
    for n, item in enumerate(c):
        if n % 2 == 1 and c[n - 1] and c[n]:
            print(current_category[number_category].max, c[n])
            if not (current_category[number_category].name == c[n - 1] and current_category[number_category].max == c[n]):
                for_save = current_category[number_category]
                print(for_save)
                for_save.name = c[n - 1]
                for_save.max = c[n]
                for_save.save()

            number_category += 1

    return render(request, 'conf.html', locals())


@csrf_exempt
def stat(request, name_url):

    configuration = request.user.settings.configurations.get(name_url=name_url)
    costs = Cost.objects.filter(costcategory__configuration=configuration).order_by('-datetime')
    max_cost = max(costs, key=lambda x: x.value, default=0)
    middle_cost = round(sum([cost.value for cost in costs]) / (datetime.now().date() - configuration.date).days)
    middle_cost_of_week = middle_cost * 8

    days = (datetime.today().date() - configuration.date).days
    now_week = days // 8
    number_days_for_week = (days // 8 + 1) * 8 - days

    if request.is_ajax():
        bool_field = configuration.category.all().get(name=request.POST['category'])
        bool_field.included_week_table = not bool_field.included_week_table
        bool_field.save()

    return render(request, 'stat.html', locals())


def cost(request, name_url):
    configuration = request.user.settings.configurations.all().get(name_url=name_url)
    tags = Tags.objects.filter(user=str(request.user)).order_by('-datetime')[:10]

    if request.POST:
        dict_value_and_comment = dict()
        for cat in configuration.category.all():
            value = 'value-' + str(cat.id)
            detailed_comment = 'detail-comment-' + str(cat.id)
            n = 0
            while True:
                complete_value = value + '-' + str(n)
                complete_detailed_comment = detailed_comment + '-' + str(n)
                try:
                    cost = Cost(value=request.POST[complete_value],
                                detailed_comment=request.POST[complete_detailed_comment])
                except KeyError:
                    break
                cost.save()

                for tag in request.POST.getlist('tags'):
                    tag_obj, b = Tags.objects.update_or_create(user=str(request.user), name=tag)
                    cost.tags.add(tag_obj)
                cat.cost.add(cost)
                n += 1

    return render(request, 'cost.html', locals())
