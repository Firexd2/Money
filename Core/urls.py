"""Money URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from Core import views1
from Core.views import actions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('panel/', views1.panel, name='panel'),
    path('panel/new/', views1.new, name='new'),
    path('<name_url>/', views1.BaseTemplateView.as_view(template_name='plan/home.html'), name='home'),
    path('<name_url>/cost/', views1.cost, name='cost'),
    path('<name_url>/stat/', views1.StatTemplateView.as_view(template_name='plan/stat.html'), name='stat'),
    path('<name_url>/settings/', views1.BaseTemplateView.as_view(template_name='plan/settings.html'), name='settings'),
    path('category/<id>/', views1.category_detail),
    path('auth/', include('Auth.urls')),



    path('ajax/correct_free_money/', actions.correct_free_money),
    path('ajax/create_new_plan/', actions.create_new_plan),
    path('ajax/start_new_period/', actions.start_new_period),
    path('ajax/edit_date/', actions.edit_date),
    path('ajax/delete_plan/', actions.delete_plan),
    path('ajax/settings_plan/', actions.settings_plan),
    path('ajax/toggle_category_week_table/', actions.toggle_category_week_table),
    path('ajax/input_cost/', actions.input_cost),
    path('ajax/delete_cost/', actions.delete_cost)
]
