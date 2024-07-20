from django.db import models


class Type(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название типа:", unique=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Types"
        verbose_name = "Тип"
        verbose_name_plural = "Типы"
