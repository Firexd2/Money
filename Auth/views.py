from django.views.generic.edit import FormView
from Auth.forms import RegisterForm
from Core.models import Settings


class RegisterFormView(FormView):
    form_class = RegisterForm
    success_url = "/panel/"
    template_name = "register.html"

    def form_valid(self, form):
        f = form.save(commit=False)
        settings = Settings()
        settings.save()
        f.settings = settings
        f.save()
        return super(RegisterFormView, self).form_valid(form)
