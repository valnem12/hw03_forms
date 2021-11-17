from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import CreationForm

from yatube.settings import LOGIN_REDIRECT_URL, LOGOUT_URL


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy(LOGIN_REDIRECT_URL)
    template_name = 'users/signup.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        username, password = (form.cleaned_data.get('username'),
                              form.cleaned_data.get('password1'))
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return HttpResponseRedirect(self.get_success_url())
        return HttpResponseRedirect(reverse(LOGOUT_URL))

