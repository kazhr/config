from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from .models import *


class TodoListAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {"widget": CheckboxSelectMultiple},
    }


# Register your models here.
admin.site.register(TodoList, TodoListAdmin)
admin.site.register(Task)
