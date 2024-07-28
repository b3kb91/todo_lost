from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, View

from accounts.forms import MyUserCreationForm, UserForm
from webapp.models import Project

User = get_user_model()


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


class UsersView(View, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'webapp.change_project'

    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        if not self.has_permission(request.user, project):
            return redirect('webapp:main')
        form = UserForm(initial={'users': project.users.all()})
        return render(request, 'user_create_project.html', {'project': project, 'form': form})

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        if not self.has_permission(request.user, project):
            return redirect('webapp:main')

        form = UserForm(request.POST)
        if form.is_valid():
            users = form.cleaned_data['users']
            project.users.set(users)
            return redirect(reverse('webapp:detail_project', kwargs={'pk': pk}))
        return render(request, 'user_create_project.html', {'project': project, 'form': form})

    def has_permission(self, user, project):
        return (user.groups.filter(name='Project Manager').exists() or
                user.groups.filter(name='Team Lead').exists() and user in project.users.all())
