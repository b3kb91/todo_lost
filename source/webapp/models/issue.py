from django.db import models
from django.urls import reverse

from webapp.models import BaseModel


class Issue(BaseModel):
    summary = models.CharField(max_length=50, null=False, blank=False, verbose_name="Краткое Описание")
    description = models.TextField(max_length=500, null=True, blank=True, verbose_name="Подробное описание",
                                   default='Пустой')
    statuses = models.ForeignKey('webapp.Status', related_name='issues', verbose_name='Статусы',
                                 on_delete=models.PROTECT)
    types = models.ManyToManyField('webapp.Type', related_name='issues', verbose_name='Типы', blank=True)
    project = models.ForeignKey('webapp.Project', null=False, blank=False, related_name='issues',
                                on_delete=models.PROTECT, verbose_name='Проект')

    def get_absolute_url(self):
        return reverse("detail", kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.summary} {self.description} {self.statuses}"

    class Meta:
        db_table = 'Issues'
        verbose_name = "Трекер задач"
        verbose_name_plural = "Трекеры задач"
