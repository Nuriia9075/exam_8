from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import AuthorCreationForm
from accounts.models import Author


class RegisterView(CreateView):
    form_class = AuthorCreationForm
    template_name = 'account/register.html'
    model = Author

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        if not next_url:
            next_url = reverse_lazy('account:login')
        return next_url