from django.db import models
import datetime


class Task(models.Model):

    class Meta:
        verbose_name = "タスク"
        verbose_name_plural = "タスク"

    name = models.CharField(
        max_length=32,
        verbose_name="タスク名"
    )

    done = models.BooleanField(
        default=False,
        verbose_name="完了"
    )

    note = models.TextField(
        blank=True,
        help_text="補足説明"
    )

    def __str__(self):
        return self.name

    def checked(self):
        """
        完了マークをつける
        """
        self.done = True
        self.save()

    def reset(self):
        """
        完了マークをはずす
        """
        self.done = False
        self.save()


class TodoList(models.Model):

    class Meta:
        verbose_name = "Todoリスト"
        verbose_name_plural = "Todoリスト"

    name = models.CharField(
        max_length=32,
        verbose_name="リスト名"
    )

    updated = models.DateField(
        auto_now=True,
        verbose_name="最終更新日"
    )

    tasks = models.ManyToManyField(
        Task,
        help_text="タスク一覧"
    )

    def __str__(self):
        return self.name

    def reset(self):
        """
        最終更新日が昨日だったら完了マークリセット
        """
        if not self.updated == datetime.date.today():
            for task in self.tasks.all():
                task.reset()

    def touch(self):
        """
        最終更新日を更新
        """
        self.save()
