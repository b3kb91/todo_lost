from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from webapp.models import Issue, Project
from webapp.forms import IssueForm


class IssueCreateView(CreateView):
    template_name = 'issues/create.html'
    form_class = IssueForm

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
        return Issue.objects.filter(deleted=False)


class IssueDeleteView(DeleteView):
    template_name = 'issues/delete.html'
    model = Issue
    success_url = reverse_lazy('webapp:main')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return self.get_success_url()


class IssueUpdateView(UpdateView):
    template_name = 'issues/update.html'
    form_class = IssueForm
    model = Issue
