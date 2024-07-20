from django.db.models import Q
from django.utils.http import urlencode
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from webapp.models import Issue
from webapp.forms import IssueForm, SearchForm


class IssueListView(ListView):
    model = Issue
    template_name = 'issues/index.html'
    context_object_name = 'issues'
    ordering = ['-updated_at']
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

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     if self.search_value:
    #         queryset = queryset.filter(
    #             Q()
    #         )
    #     return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.search_value:
            context["search"] = urlencode({"search": self.search_value})
            context["search_value"] = self.search_value
        return context


class IssueDetailView(DetailView):
    def dispatch(self, request, *args, **kwargs):
        self.issue = get_object_or_404(Issue, pk=kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["issue"] = self.issue
        return context

    def get_template_names(self):
        return "detail.html"


class CreateIssueView(CreateView):
    model = Issue
    form_class = IssueForm
    template_name = 'projects'
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = IssueForm()
        return render(request, 'issues/create.html', context={"form": form})

    def post(self, request, *args, **kwargs):
        form = IssueForm(data=request.POST)

        if form.is_valid():
            issue = form.save()
            return redirect('detail', pk=issue.pk)

        return render(
            request,
            "issues/create.html",
            {"form": form})


class DeleteIssueView(View):

    def dispatch(self, request, *args, **kwargs):
        self.issue = get_object_or_404(Issue, pk=kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, "issues/delete.html", context={"issue": self.issue})

    def post(self, request, *args, **kwargs):
        self.issue.delete()
        return redirect("main")


class UpdateIssueView(View):
    def dispatch(self, request, *args, **kwargs):
        self.issue = get_object_or_404(Issue, pk=kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = IssueForm(instance=self.issue)
        return render(
            request, "issues/update.html",
            context={"form": form})

    def post(self, request, *args, **kwargs):
        form = IssueForm(data=request.POST, instance=self.issue)
        if form.is_valid():
            issue = form.save()
            return redirect("detail", pk=issue.pk)
        else:
            return render(
                request,
                "issues/update.html",
                {"form": form})
