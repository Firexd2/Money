from django.shortcuts import render


def create_configuration(request):

    return render(request, 'new_configuration.html', locals())
