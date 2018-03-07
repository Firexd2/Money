import json
from datetime import datetime
from math import floor
from django.http import HttpResponse
from Core.models import Configuration, CostCategory, Cost, Tags





def correct_free_money(request):
    if request.POST:
        settings = request.user.settings
        settings.free_money = request.POST['value']
        settings.save()
        return HttpResponse('ok')


def create_new_plan(request):
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

        # h = History(description='')
        # configuration.history.add(h)

        return HttpResponse('ok')


def start_new_period(request):
    configuration = request.user.settings.configurations.all().get(name_url=request.POST['name'])
    if request.POST:
        last_income = configuration.income

        balance = last_income - sum(
            list(map(lambda x: x.value, Cost.objects.filter(costcategory__configuration=configuration))))
        configuration.income = int(request.POST['income'])
        configuration.date = datetime.now().date()
        configuration.save()
        settings = configuration.settings_set.all()[0]
        settings.free_money += balance
        settings.save()

        count_category = configuration.category.all().count()

        distribution = (int(request.POST['income']) - last_income) / count_category

        if distribution == int(distribution):
            list_values_add = [distribution] * count_category
        else:
            list_values_add = [floor(distribution)] * count_category
            list_values_add[-1] += int(request.POST['income']) - last_income - (floor(distribution) * count_category)

        for n, category in enumerate(configuration.category.all()):
            category.cost.all().delete()
            cat = category
            cat.max += list_values_add[n]
            cat.save()

        response = {'status': 1, 'balance': balance}

    return HttpResponse(json.dumps(response), content_type='application/json')


def edit_date(request):
    configuration = request.user.settings.configurations.all().get(name_url=request.POST['name'])
    if request.POST:
        date = datetime.strptime(request.POST['date'], '%Y-%m-%d').date()
        status = 0
        if datetime.now().date() >= date:
            configuration.date = date
            configuration.save()
            status = 1
        response = {'status': status}

    return HttpResponse(json.dumps(response), content_type='application/json')


def delete_plan(request):
    configuration = request.user.settings.configurations.all().get(name_url=request.POST['name'])
    if request.POST:
        balance = configuration.income - sum(
            list(map(lambda x: x.value, Cost.objects.filter(costcategory__configuration=configuration))))
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


def settings_plan(request):

    configuration = request.user.settings.configurations.all().get(id=request.POST['id'])

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

        return HttpResponse('ok')


def toggle_category_week_table(request):
    configuration = request.user.settings.configurations.get(name_url=request.POST['name'])

    bool_field = configuration.category.all().get(name=request.POST['category'])
    bool_field.included_week_table = not bool_field.included_week_table
    bool_field.save()

    return HttpResponse('ok')


def input_cost(request):
    configuration = request.user.settings.configurations.get(name_url=request.POST['name'])

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

    return HttpResponse('ok')


def delete_cost(request):
    configuration = request.user.settings.configurations.all().get(name_url=request.POST['name'])
    Cost.objects.filter(costcategory__configuration=configuration)\
        .order_by('-datetime').get(id=request.POST['id']).delete()

    return HttpResponse('ok')


def archiving(name, *args):

    pass
