from datetime import datetime

from django.db import models, connection

from django.urls import reverse
from django.utils import timezone


class Thematic(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удалена'),
    )

    name = models.CharField(max_length=100, verbose_name="Название")
    status = models.IntegerField(max_length=100, choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    description = models.TextField(max_length=500, verbose_name="Описание")
    image = models.ImageField(upload_to="thematics", default="thematics/default.png", verbose_name="Фото")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тематика"
        verbose_name_plural = "Тематики"

    def get_absolute_url(self):
        return reverse("thematic_details", kwargs={"thematic_id": self.id})

    def get_delete_url(self):
        return reverse("thematic_delete", kwargs={"thematic_id": self.id})

    def delete(self):
        with connection.cursor() as cursor:
            cursor.execute("UPDATE exhibitions_thematic SET status = 2 WHERE id = %s", [self.pk])


class Exhibition(models.Model):
    STATUS_CHOICES = (
        (1, 'Введён'),
        (2, 'В работе'),
        (3, 'Завершён'),
        (4, 'Отменён'),
        (5, 'Удалён'),
    )

    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(max_length=500, verbose_name="Описание")
    room = models.CharField(max_length=100, verbose_name="Помещение")
    thematics = models.ManyToManyField(Thematic, verbose_name="Выставки", null=True)
    date = models.TimeField(default=datetime.now(tz=timezone.utc), verbose_name="Время")

    status = models.IntegerField(max_length=100, choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    date_created = models.DateTimeField(default=datetime.now(tz=timezone.utc), verbose_name="Дата создания")
    date_of_formation = models.DateTimeField(default=datetime.now(tz=timezone.utc), verbose_name="Дата формирования")
    date_complete = models.DateTimeField(default=datetime.now(tz=timezone.utc), verbose_name="Дата завершения")

    def __str__(self):
        return "Выставка №" + str(self.pk)

    class Meta:
        verbose_name = "Выставка"
        verbose_name_plural = "Выставки"