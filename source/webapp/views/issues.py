from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView
from webapp.models import Issue
from webapp.forms import IssueForm


class IssueDetailView(DetailView):
    template_name = 'issues/detail.html'
    model = Issue

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["comments"] = self.object.comments.order_by("-created_at")
    #     return context


class IssueDeleteView(DeleteView):
    template_name = 'issues/delete.html'
    model = Issue
    success_url = reverse_lazy('main')
    # queryset = Issue.objects.all()
    #
    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     self.object.delete()
    #     return redirect("detail", pk=self.object.issue.pk)


class IssueUpdateView(UpdateView):
    template_name = 'issues/update.html'
    form_class = IssueForm
    model = Issue
