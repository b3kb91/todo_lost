from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from webapp.models import Issue, Project
from webapp.forms import IssueForm


# /issue/12/

class IssueCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'issues/create.html'
    form_class = IssueForm
    permission_required = 'webapp.add_issue'

    def has_permission(self):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        return (self.request.user.groups.filter(name='Project Manager').exists() or
                self.request.user.groups.filter(name='Team Lead').exists() or
                self.request.user.groups.filter(name='Developer').exists()
                and self.request.user in project.users.all())

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        issue = form.save(commit=False)
        issue.project = project
        issue.save()
        return redirect(project.get_absolute_url())


class IssueDetailView(DetailView):
    template_name = 'issues/detail.html'
    model = Issue

    def get_queryset(self):
        return Issue.objects.filter(is_deleted=False)


class IssueDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'issues/delete.html'
    model = Issue
    success_url = reverse_lazy('webapp:main')
    permission_required = 'webapp.delete_issue'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return self.get_success_url()

    def has_permission(self):
        issue = self.get_object()
        return (self.request.user.groups.filter(name='Project Manager').exists() or
                self.request.user.groups.filter(name='Team Lead').exists()
                and self.request.user in issue.users.all())


class IssueUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'issues/update.html'
    form_class = IssueForm
    model = Issue
    permission_required = 'webapp.change_issue'

    def has_permission(self):
        issue = self.get_object()
        return (self.request.user.groups.filter(name='Project Manager').exists() or
                self.request.user.groups.filter(name='Team Lead').exists() or
                self.request.user.groups.filter(name='Developer').exists()
                and self.request.user in issue.users.all())
