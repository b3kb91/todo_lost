from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from django.views.generic import TemplateView

from webapp.models import Issue
from webapp.forms import IssueForm


class IssueListView(TemplateView):
    # template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        issue = Issue.objects.order_by('-updated_at')
        return render(request, 'index.html', context={"issue": issue})


class IssueDetailView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        self.issue = get_object_or_404(Issue, pk=kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["issue"] = self.issue
        return context

    def get_template_names(self):
        return "detail.html"


class CreateIssueView(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = IssueForm()
        return render(request, 'create.html', context={"form": form})

    def post(self, request, *args, **kwargs):
        form = IssueForm(data=request.POST)

        if form.is_valid():
            issue = form.save()
            return redirect('detail', pk=issue.pk)

        return render(
            request,
            "create.html",
            {"form": form})


class DeleteIssueView(View):

    def dispatch(self, request, *args, **kwargs):
        self.issue = get_object_or_404(Issue, pk=kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, "delete.html", context={"issue": self.issue})

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
            request, "update.html",
            context={"form": form})

    def post(self, request, *args, **kwargs):
        form = IssueForm(data=request.POST, instance=self.issue)
        if form.is_valid():
            issue = form.save()
            return redirect("detail", pk=issue.pk)
        else:
            return render(
                request,
                "update.html",
                {"form": form})
