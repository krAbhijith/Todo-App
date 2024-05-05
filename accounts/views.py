from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, RedirectView, View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password

from django.contrib.auth.models import User


class RegisterView(CreateView):
    model = User
    fields = ['first_name', 'email']
    template_name = 'accounts/form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        password = self.request.POST.get('password')
        form.instance.username = self.request.POST.get('email')
        form.instance.password = make_password(password)

        self.object = form.save()
        login(self.request, self.object)
        return HttpResponseRedirect(self.get_success_url())
    

class LoginView(View):

    def post(self, request, *args, **kwargs):
        username = self.request.POST.get('email')
        password = self.request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('register')
        

class LogoutView(RedirectView):
    query_string = False
    pattern_name = 'register'

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return reverse_lazy(self.pattern_name)
    