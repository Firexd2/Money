from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from Core.models import Configuration, CostCategory


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
    return render(request, 'conf.html', locals())
