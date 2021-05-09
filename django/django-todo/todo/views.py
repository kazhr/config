# from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from .models import TodoList, Task
import datetime


# Create your views here.
class TodoListListView(generic.ListView):

    model = TodoList


class TodoListDetailView(generic.DetailView):

    model = TodoList

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_todolist = TodoList.objects.get(pk=self.kwargs["pk"])
        if not selected_todolist.updated == datetime.date.today():
            for task in selected_todolist.tasks.all():
                task.reset()

        return context


def checked(request, pk):

    task_pk = [int(k) for k, v in request.POST.items() if v == "Check"][0]
    task = get_object_or_404(Task, pk=task_pk)
    task.checked()

    return HttpResponseRedirect(reverse("detail", args=(pk,)))
