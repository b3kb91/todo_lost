from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView

from accounts.forms import MyUserCreationForm

User = get_user_model()


# Create your views here.

def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_path = request.POST.get('next', "webapp:main")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(next_path, "next_path")
            return redirect(next_path)
        else:
            context['has_error'] = True
    context["next_param"] = request.GET.get('next')
    return render(request, 'login.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('webapp:main')


class RegistrationView(CreateView):
    form_class = MyUserCreationForm
    template_name = 'registration.html'
    model = User

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('webapp:main')
        return next_url
