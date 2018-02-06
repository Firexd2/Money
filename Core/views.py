from django.shortcuts import render


def home(request):
    return render(request, 'home.html', locals())


def create_configuration(request):

    return render(request, 'new.html', locals())
