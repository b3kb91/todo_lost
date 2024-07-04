from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect

from webapp.forms import ToDoForm
from webapp.models import ToDo, status_choices
from webapp.forms import ToDoForm


def index(request):
    todos = ToDo.objects.order_by('-date_completion')
    return render(request, 'index.html', context={"todos": todos})


def create_todo(request):
    if request.method == "GET":
        form = ToDoForm()
        return render(request, 'create_todo.html', context={"form": form})
    else:
        form = ToDoForm(request.POST)
        if form.is_valid():
            if form.is_valid():
                todo = form.save()
                return redirect('todo_detail', pk=todo.pk)

            return render(
                request,
                "create_todo.html",
                {"form": form}
            )


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


def todo_update(request, *args, pk, **kwargs):
    todo = get_object_or_404(ToDo, pk=pk)
    if request.method == "GET":
        form = ToDoForm(instance=todo)
        return render(
            request, "update_todo.html"
            , context={"form": form}
        )
    else:
        form = ToDoForm(data=request.POST, instance=todo)
        if form.is_valid():
            todo = form.save()
            return redirect("todo_detail", pk=todo.pk)
        else:
            return render(
                request,
                "update_todo.html",
                {"form": form}
            )
