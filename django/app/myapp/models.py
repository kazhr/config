import datetime
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _

# Create your models here.


class Tag(models.Model):

    date = models.DateField()


class Note(models.Model):

    name = models.CharField(
        max_length=32,
    )

    def update_note_name(self, name):
        self.name = name
        if self.name == "":
            raise ValidationError(
                _("name must not be blank."),
                code="invalid"
            )

        self.full_clean()
        self.save()

    def get_or_create_today():
        date = Tag.objects.get_or_create(date=datetime.date.today())
        return date

    date = models.ForeignKey(
        Tag,
        default=get_or_create_today,
        on_delete=models.CASCADE
    )
