from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from Core.models import Configuration, CostCategory


@login_required
def home(request):
    return render(request, 'home.html', locals())


@login_required
def new(request):
    if request.POST:
        configuration = Configuration(name=request.POST['name'], income=request.POST['income'])
        configuration.save()

        c = [item[1] for item in request.POST.items()][3:]

        for n, item in enumerate(c):
            if n % 2 == 1 and c[n-1] and c[n]:
                cost_category = CostCategory(name=c[n-1], max=c[n])
                cost_category.save()
                configuration.category.add(cost_category)
        request.user.settings.configurations.add(configuration)

        return redirect('home')

    return render(request, 'new.html', locals())
