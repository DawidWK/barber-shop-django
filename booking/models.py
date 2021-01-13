from django.db import models
from datetime import datetime, date, time, timedelta
from django.core.validators import MaxValueValidator, MinValueValidator
import json

# Create your models here.
schedule_template = '''
{
    "schedule_day": [
        {
            "start": 8,
            "end": 16
        }
    ]
}
'''

services_choices = [
    ("HAIR", "HAIR CUT"),
    ("WAX", "WAX"),
    ("SHAVE", "SHAVE")
]

class Barber(models.Model):
    name = models.CharField(max_length=30)
    start_time = models.IntegerField(default=8, validators=[MaxValueValidator(16), MinValueValidator(0)])
    JSON_schedule_template = schedule_template
    schedule = models.TextField(default=JSON_schedule_template)
    photo = models.ImageField(upload_to='barber_avatar', default='default.png')

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(max_length=30)
    barber = models.ForeignKey(to='Barber', on_delete=models.CASCADE)
    service = models.CharField(max_length=16, choices=services_choices, default="HAIR")
    start_time = models.IntegerField()

    def __str__(self):
        return self.name