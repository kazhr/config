from django.db import models

# Create your models here.
class Task(models.Model):

    class Meta:
        verbose_name = "タスク"
        verbose_name_plural = "タスク"

    name = models.CharField(
        max_length=32,
        help_text="タスク名"
    )

    done = models.BooleanField(
        default=False,
        verbose_name="完了"
    )

    def checked(self):
        self.done = True
        self.save()

        # update the last modified date
        for todolist in self.todolist_set.all():
            todolist.save()

    def reset(self):
        self.done = False
        self.save()

    note = models.TextField(
        blank=True,
        help_text="ノート"
    )

    def __str__(self):
        return self.name


class TodoList(models.Model):

    class Meta:
        verbose_name = "Todoリスト"
        verbose_name_plural = "Todoリスト"

    name = models.CharField(
        max_length=32,
        help_text="リスト名"
    )

    updated = models.DateField(
        auto_now=True,
        help_text="最終更新日"
    )

    tasks = models.ManyToManyField(
        Task,
        # on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
