from django.db.models import Q
from django.utils.http import urlencode
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from webapp.models import Project
from webapp.forms import SearchForm, ProjectForm


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project.html'
    context_object_name = 'projects'
    ordering = ['-start_date']
    paginate_by = 5

    def dispatch(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.search_value = self.get_search_value()
        return super().dispatch(*args, **kwargs)

    def get_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        form = self.form
        if form.is_valid():
            return form.cleaned_data['search']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            queryset = queryset.filter(
                Q(title__contains=self.search_value) | Q(description__contains=self.search_value)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.search_value:
            context["search"] = urlencode({"search": self.search_value})
            context["search_value"] = self.search_value
        return context


class ProjectDetailView(DetailView):
    template_name = "projects/detail_project.html"
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projects"] = self.object.projects.order_by('-start_date')
        return context


class CreateProjectView(CreateView):
    model = Project
    template_name = 'projects/create_project.html'
    form_class = ProjectForm

    def get_success_url(self):
        return redirect("detail_project",  kwargs={'pk': self.object.pk})

