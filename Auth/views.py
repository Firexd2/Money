from django.views.generic.edit import FormView
from Auth.forms import RegisterForm


class RegisterFormView(FormView):
    form_class = RegisterForm
    success_url = "/"
    template_name = "register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)
