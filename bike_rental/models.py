from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


""" 
Модель велосипедов для аренды
"""


class BikeModel(models.Model):
    STATUS_CHOICES = (
        ('available', 'Доступен для аренды'),
        ('unavailable', 'Арендован')
    )
    BIKE_TYPE_CHOICES = (
        ('urban', 'Городские'),
        ('road', 'Шоссейные'),
        ('off-reoad', 'Внедорожные')
    )

    name = models.CharField(
        max_length=128,
        verbose_name='Модель велосипеда'
    )
    bike_type = models.CharField(
        max_length=128,
        choices=BIKE_TYPE_CHOICES,
        verbose_name='Тип велосипеда'
    )
    status = models.CharField(
        max_length=64,
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES[0],
        verbose_name='Статус'
    )

    def __str__(self):
        return self.name


""" 
Модель аренды велосипедов
"""


class BikeRentalModel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    bike = models.ForeignKey(
        BikeModel,
        on_delete=models.CASCADE,
        verbose_name='Модель велосипеда'
    )
    rental_start = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время начала аренды'
    )
    rental_end = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Время окончания аренды'
    )

    # def end_bike_rental(self):
    #     self.rental_end = timezone.now()
    #     self.save()
    #     self.bike.status = 'available'
    #     self.bike.save()

    # def calculate_rental_cost(self):
    #     rental_duration = self.rental_end - self.rental_start
    #     cost_per_hour = 10
    #     hours = rental_duration.total_seconds() / 3600
    #     return round(hours * cost_per_hour, 2)

    def __str__(self):
        return f"{self.user.username} rented {self.bike.name}"
