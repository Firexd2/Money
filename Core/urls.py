"""
Money URL Configuration

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
from Core.models import Archive, ShoppingListItem, ShoppingList, HelpText, VersionControl, CostCategory
from Core.views import actions, views
from django.views.generic import RedirectView, ListView, DetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_tools/', include('admin_tools.urls')),
    path('', RedirectView.as_view(url='/panel/')),
    path('favicon.ico/', RedirectView.as_view(url='/static/image/favicon.ico'), name='favicon'),
    path('panel/', views.BaseTemplateView.as_view(template_name='panel/base.html'), name='panel'),
    path('panel/home/', views.BaseTemplateView.as_view(template_name='panel/panel.html')),
    path('panel/new/', views.BaseTemplateView.as_view(template_name='panel/new.html')),
    path('panel/about/', views.TemplateView.as_view(template_name='panel/about.html')),
    path('panel/help/', ListView.as_view(template_name='panel/help.html', model=HelpText)),
    path('panel/version/', ListView.as_view(template_name='panel/version.html', model=VersionControl)),
    path('panel/new_version/', ListView.as_view(template_name='panel/version.html', model=VersionControl)),
    path('<name>/', views.BaseTemplatePlanView.as_view(template_name='plan/base.html'), name='base'),
    path('<name>/home/', views.BaseTemplatePlanView.as_view(template_name='plan/home.html')),
    path('<name>/cost/', views.CostTemplatePlanView.as_view(template_name='plan/cost.html')),
    path('<name>/stat/', views.StatTemplatePlanView.as_view(template_name='plan/stat/stat.html')),
    path('<name>/shopping_list/', views.ShoppingListTemplateView.as_view(template_name='plan/shopping_list/shopping_list.html')),
    path('<name>/shopping_list/<id>/', views.DetailShoppingListTemplateView.as_view(template_name='plan/shopping_list/create_shopping_list.html')),
    path('<name>/settings/', views.BaseTemplatePlanView.as_view(template_name='plan/settings.html')),
    path('<name>/archive/', views.ArchiveTemplatePlanView.as_view(template_name='plan/archive/archive.html')),
    path('<name>/archive/<date_one>/<date_two>/', views.ArchiveReportLastPeriodView.as_view(template_name='plan/archive/report_last_period.html')),
    path('<name>/archive/<type_date>/', views.GetDatesInArchive.as_view()),
    path('archive/detail/<int:pk>/', DetailView.as_view(template_name='plan/archive/detail_archive.html', model=Archive), name='detail_archive'),
    path('alert/change_date/', views.TemplateView.as_view(template_name='plan/archive/change_date_alert.html')),
    path('category/<pk>/', DetailView.as_view(template_name='plan/stat/category_detail.html', model=CostCategory)),
    path('table_input/<pk>/', DetailView.as_view(template_name='plan/shopping_list/table_input.html', model=ShoppingList)),
    path('tag/<name>/<tag>/', views.TagDetailView.as_view(template_name='plan/stat/tag_detail.html')),
    path('auth/', include('Auth.urls')),
    path('help/<name>/', views.GetHelpText.as_view(template_name='help.html')),

    path('ajax/create_new_plan/', actions.CreateNewPlan.as_view()),
    path('ajax/start_new_period/', actions.StartNewPeriod.as_view()),
    path('ajax/middle_icone_plan/', actions.InputMiddleIncomePlan.as_view()),
    path('ajax/delete_plan/', actions.DeletePlan.as_view()),
    path('ajax/settings_plan/', actions.SettingsPlan.as_view()),
    path('ajax/toggle_category_week_table/', actions.ToggleCategoryWeekTable.as_view()),
    path('ajax/input_cost/', actions.InputCost.as_view()),
    path('ajax/delete_cost/', actions.DeleteCost.as_view()),
    path('ajax/new_shopping_list/', actions.CreateShoppingList.as_view()),
    path('ajax/delete_item_shopping_list/<id>/', actions.DeleteItem.as_view(model=ShoppingListItem)),
    path('ajax/delete_shopping_list/<id>/', actions.DeleteItem.as_view(model=ShoppingList)),
    path('ajax/input_cost_shopping_list/<id>/', actions.InputCostShoppingList.as_view()),
    path('ajax/add_money/', actions.AddIncome.as_view()),
    path('ajax/take_money/', actions.TakeIncome.as_view()),
    path('ajax/first_log_in/', actions.first_log_in_trigger),
    path('ajax/look_last_version/', actions.look_last_version)
]
