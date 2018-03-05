import json
from datetime import datetime
from math import floor
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from Core.models import Configuration, CostCategory, Cost, Tags


@login_required
def panel(request):

    money_circulation = sum([conf.income for conf in request.user.settings.configurations.all()])

    if request.is_ajax():
        settings = request.user.settings
        settings.free_money = request.POST['value']
        settings.save()

    return render(request, 'panel/panel.html', locals())


@login_required
def new(request):
    if request.POST:
        configuration = Configuration(name=request.POST['name'], income=request.POST['income'],
                                      icon=request.POST['icon'], color=request.POST['color'])
        configuration.save()
        c = [item[1] for item in request.POST.items()][4:]
        for n, item in enumerate(c):
            if n % 2 == 1 and c[n - 1] and c[n]:
                cost_category = CostCategory(name=c[n - 1], max=c[n])
                cost_category.save()
                configuration.category.add(cost_category)
        request.user.settings.configurations.add(configuration)
        return redirect('panel')
    return render(request, 'panel/new.html', locals())


def home(request, name_url):
    configuration = request.user.settings.configurations.all().get(name_url=name_url)
    if request.is_ajax():
        POST = request.POST
        if 'income' in POST:

            last_income = configuration.income

            balance = last_income - \
                      sum(list(map(lambda x: x.value, Cost.objects.filter(costcategory__configuration=configuration))))
            configuration.income = int(POST['income'])
            configuration.date = datetime.now().date()
            configuration.save()
            settings = configuration.settings_set.all()[0]
            settings.free_money += balance
            settings.save()

            count_category = configuration.category.all().count()

            distribution = (int(POST['income']) - last_income) / count_category

            if distribution == int(distribution):
                list_values_add = [distribution] * count_category
            else:
                list_values_add = [floor(distribution)] * count_category
                list_values_add[-1] += int(POST['income']) - last_income - (floor(distribution) * count_category)

            for n, category in enumerate(configuration.category.all()):
                category.cost.all().delete()
                cat = category
                cat.max += list_values_add[n]
                cat.save()

            response = {'status': 1, 'balance': balance}

        elif 'date' in POST:
            date = datetime.strptime(POST['date'], '%Y-%m-%d').date()
            status = 0
            if datetime.now().date() >= date:
                configuration.date = date
                configuration.save()
                status = 1
            response = {'status': status}

        elif 'delete' in POST:
            balance = configuration.income - \
                      sum(list(map(lambda x: x.value, Cost.objects.filter(costcategory__configuration=configuration))))
            settings = configuration.settings_set.all()[0]
            settings.free_money += balance
            settings.save()
            try:
                configuration.delete()
                status = 1
            except:
                status = 0
            response = {'status': status}

        return HttpResponse(json.dumps(response), content_type='application/json')

    return render(request, 'conf/home.html', locals())


def settings(request, name_url):

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
                if not (current_category[number_category].name == c[n - 1] and current_category[number_category].max == c[n]):
                    for_save = current_category[number_category]
                    for_save.name = c[n - 1]
                    for_save.max = c[n]
                    for_save.save()
                number_category += 1
        return redirect(configuration.get_absolute_url())

    return render(request, 'conf/settings.html', locals())


def category_detail(request, id):
    category = CostCategory.objects.get(id=id)
    return render(request, 'conf/category_detail.html', locals())


def stat(request, name_url):

    configuration = request.user.settings.configurations.get(name_url=name_url)
    costs = Cost.objects.filter(costcategory__configuration=configuration).order_by('-datetime')
    max_cost = max(costs, key=lambda x: x.value, default=0)
    middle_cost = round(sum([cost.value for cost in costs]) / ((datetime.now().date() - configuration.date).days + 1))
    middle_cost_of_week = middle_cost * 8

    days = (datetime.today().date() - configuration.date).days
    now_week = days // 8
    number_days_for_week = (days // 8 + 1) * 8 - days

    if request.is_ajax():
        bool_field = configuration.category.all().get(name=request.POST['category'])
        bool_field.included_week_table = not bool_field.included_week_table
        bool_field.save()

    return render(request, 'conf/stat.html', locals())


def cost(request, name_url):
    configuration = request.user.settings.configurations.all().get(name_url=name_url)
    costs = Cost.objects.filter(costcategory__configuration=configuration).order_by('-datetime')
    tags = Tags.objects.filter(user=str(request.user)).order_by('-datetime')[:10]

    if request.is_ajax():
        costs.get(id=request.POST['id']).delete()

    if request.POST and not request.is_ajax():
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

    return render(request, 'conf/cost.html', locals())
