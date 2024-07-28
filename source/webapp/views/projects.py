from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.utils.http import urlencode
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from webapp.models import Project
from webapp.forms import SearchForm, ProjectForm


# /project/25/delete/
class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project.html'
    context_object_name = 'projects'
    ordering = ['-start_date']
    paginate_by = 5

    def dispatch(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.search_value = self.get_search_value()
        return super().dispatch(request, *args, **kwargs)

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
                Q(title__icontains=self.search_value) | Q(description__icontains=self.search_value)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.form
        if self.search_value:
            context["search"] = urlencode({"search": self.search_value})
            context["search_value"] = self.search_value
        return context


class ProjectDetailView(DetailView):
    template_name = "projects/detail_project.html"
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["issues"] = self.object.issues.order_by('-summary')
        return context


class ProjectCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'projects/create_project.html'
    form_class = ProjectForm
    permission_required = 'webapp.add_project'

    def has_permission(self):
        return self.request.user.groups.filter(name='Project Manager').exists()

    def form_valid(self, form):
        project = form.save(commit=False)
        project.save()
        project.users.add(self.request.user)
        return super().form_valid(form)


class ProjectUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'projects/update_project.html'
    model = Project
    form_class = ProjectForm
    permission_required = 'webapp.change_project'

    def has_permission(self):
        project = self.get_object()
        return (self.request.user.groups.filter(name='Project Manager').exists() and
                self.request.user in project.users.all())


class ProjectDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'projects/delete_project.html'
    model = Project
    success_url = reverse_lazy('webapp:main')
    permission_required = 'webapp.delete_project'

    def has_permission(self):
        project = self.get_object()
        return (self.request.user.groups.filter(name='Project Manager').exists() and
                self.request.user in project.users.all())
