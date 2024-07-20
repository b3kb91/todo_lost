from django.db import models


class Status(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название статуса:", unique=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Statuses"
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
