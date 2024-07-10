from django.shortcuts import render, redirect, get_object_or_404

from webapp.models import Issue
from webapp.forms import IssueForm


def index(request):
    issue = Issue.objects.order_by('-updated_at')
    return render(request, 'index.html', context={"issue": issue})


def create_issue(request):
    if request.method == "GET":
        form = IssueForm()
        return render(request, 'create.html', context={"form": form})
    else:
        form = IssueForm(request.POST)
        if form.is_valid():
            if form.is_valid():
                issue = form.save()
                return redirect('detail', pk=issue.pk)

            return render(
                request,
                "create.html",
                {"form": form}
            )


def delete_issue(request, *args, pk, **kwargs):
    issue = get_object_or_404(Issue, pk=pk)
    if request.method == "GET":
        return render(request, "delete.html", context={"issue": issue})
    else:
        issue.delete()
        return redirect("main")


def detail_issue(request, *args, pk, **kwargs):
    issue = get_object_or_404(Issue, pk=pk)
    return render(request, "detail.html", context={"issue": issue})


def update_issue(request, *args, pk, **kwargs):
    issue = get_object_or_404(Issue, pk=pk)
    if request.method == "GET":
        form = IssueForm(instance=issue)
        return render(
            request, "update.html",
            context={"form": form}
        )
    else:
        form = IssueForm(data=request.POST, instance=issue)
        if form.is_valid():
            issue = form.save()
            return redirect("detail", pk=issue.pk)
        else:
            return render(
                request,
                "update.html",
                {"form": form}
            )
