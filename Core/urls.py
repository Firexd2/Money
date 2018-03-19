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
from django.views.generic import RedirectView

from Core.models import Archive
from Core.views import actions, views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico/', RedirectView.as_view(url='/static/images/favicon.ico'), name='favicon'),
    path('panel/', views.BaseTemplateView.as_view(template_name='panel/base.html'), name='panel'),
    path('panel/home/', views.BaseTemplateView.as_view(template_name='panel/panel.html')),
    path('panel/new/', views.BaseTemplateView.as_view(template_name='panel/new.html')),
    path('<name_url>/', views.BaseTemplatePlanView.as_view(template_name='plan/base.html'), name='base'),
    path('<name_url>/home/', views.BaseTemplatePlanView.as_view(template_name='plan/home.html')),
    path('<name_url>/cost/', views.CostTemplatePlanView.as_view(template_name='plan/cost.html')),
    path('<name_url>/stat/', views.StatTemplatePlanView.as_view(template_name='plan/stat/stat.html')),
    path('<name_url>/shopping_list/', views.ShoppingListTemplateView.as_view(template_name='plan/shopping_list/shopping_list.html')),
    path('<name_url>/shopping_list/<id>/', views.DetailShoppingListTemplateView.as_view(template_name='plan/shopping_list/create_shopping_list.html')),
    path('<name_url>/settings/', views.BaseTemplatePlanView.as_view(template_name='plan/settings.html')),
    path('<name_url>/archive/', views.ArchiveTemplatePlanView.as_view(template_name='plan/archive/archive.html')),
    path('<name_url>/archive/<date_one>/<date_two>/', views.ArchiveReportLastPeriodView.as_view(template_name='plan/archive/report_last_period.html')),
    path('<name_url>/archive/<type_date>/', views.GetDatesInArchive.as_view()),
    path('archive/detail/<int:pk>/', views.DetailView.as_view(template_name='plan/archive/detail_archive.html', model=Archive), name='detail_archive'),
    path('alert/change_date/', views.TemplateView.as_view(template_name='plan/archive/change_date_alert.html')),
    path('category/<id>/', views.CategoryDetailView.as_view(template_name='plan/stat/category_detail.html')),
    path('tag/<name_url>/<name>/', views.TagDetailView.as_view(template_name='plan/stat/tag_detail.html')),
    path('auth/', include('Auth.urls')),

    path('ajax/correct_free_money/', actions.CorrectFreeMoney.as_view()),
    path('ajax/create_new_plan/', actions.CreateNewPlan.as_view()),
    path('ajax/start_new_period/', actions.StartNewPeriod.as_view()),
    path('ajax/edit_date/', actions.EditDate.as_view()),
    path('ajax/delete_plan/', actions.DeletePlan.as_view()),
    path('ajax/settings_plan/', actions.SettingsPlan.as_view()),
    path('ajax/toggle_category_week_table/', actions.ToggleCategoryWeekTable.as_view()),
    path('ajax/input_cost/', actions.InputCost.as_view()),
    path('ajax/delete_cost/', actions.DeleteCost.as_view()),
    path('ajax/new_shopping_list/', actions.CreateShoppingList.as_view()),
    path('ajax/delete_item_shopping_list/<id>/', actions.DeleteItemShoppingList.as_view()),
]
