from django.urls import path
from django.contrib.auth import views as auth_views
from Auth import views


urlpatterns = [
    path('register/', views.RegisterFormView.as_view()),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name='user_login')
]
