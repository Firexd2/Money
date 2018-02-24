from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from Core.models import Configuration, CostCategory, Cost, Tags


@login_required
def panel(request):
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
    return render(request, 'conf.html', locals())


@csrf_exempt
def stat(request, name_url):
    configuration = request.user.settings.configurations.all().get(name_url=name_url)
    last_cost = Cost.objects.filter(costcategory__configuration=configuration).order_by('-datetime')

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
