from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect

from webapp.models import ToDo, status_choices


def index(request):
    todos = ToDo.objects.order_by('-date_completion')
    return render(request, 'index.html', context={"todos": todos})


def create_todo(request):
    if request.method == "GET":
        return render(request, "create_todo.html", {"status_choices": status_choices})
    else:
        date_completion = request.POST.get("date_completion")
        if date_completion == '':
            date_completion = None
        description_detail = request.POST.get("description_detail")
        if description_detail == '':
            description_detail = None

        todo = ToDo.objects.create(
            description_detail=description_detail,
            description=request.POST.get("description"),
            status=request.POST.get("status"),
            date_completion=date_completion
        )
        return redirect("todo_detail", pk=todo.pk)


def todo_delete(request, *args, pk, **kwargs):
    todo = get_object_or_404(ToDo, pk=pk)
    if request.method == "GET":
        return render(request, "delete_todo.html", context={"todo": todo})
    else:
        todo.delete()
        return redirect("todo")


def todo_detail(request, *args, pk, **kwargs):
    todo = get_object_or_404(ToDo, pk=pk)
    return render(request, "todo_detail.html", context={"todo": todo})
