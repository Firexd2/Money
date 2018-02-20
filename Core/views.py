from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from Core.models import Configuration, CostCategory, Cost


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
            if n % 2 == 1 and c[n-1] and c[n]:
                cost_category = CostCategory(name=c[n-1], max=c[n])
                cost_category.save()
                configuration.category.add(cost_category)
        request.user.settings.configurations.add(configuration)

        return redirect('panel')

    return render(request, 'new.html', locals())


def conf(request, name_url):
    configuration = request.user.settings.configurations.all().get(name_url=name_url)

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
                                detailed_comment=request.POST[complete_detailed_comment],
                                comment=request.POST['common-comment'])
                except KeyError:
                    break
                cost.save()
                cat.cost.add(cost)
                n += 1

    return render(request, 'conf.html', locals())
