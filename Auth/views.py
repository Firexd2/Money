from django.views.generic.edit import FormView

from Auth.forms import RegisterForm
from Core.models import Settings, VersionControl


class RegisterFormView(FormView):
    form_class = RegisterForm
    success_url = "/panel/"
    template_name = "register.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        settings = Settings()
        settings.save()
        user.settings = settings
        user.look_version = VersionControl.objects.all().last()
        user.save()
        return super(RegisterFormView, self).form_valid(form)
