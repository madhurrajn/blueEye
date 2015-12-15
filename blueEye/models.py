from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class CellInfo(models.Model):
    cell_name = models.CharField(max_length=100, primary_key=True)
    def __unicode__(self):
        return str(self.pk)
    azimuth = models.IntegerField(
        default=65,
        validators=[
            MaxValueValidator(359),
            MinValueValidator(0)
        ]
    )
    radius = models.IntegerField(
        default=5,
        validators=[
            MaxValueValidator(50),
            MinValueValidator(1)
        ]
    )
    beamwidth = models.IntegerField(
        default=65,
        validators=[
            MaxValueValidator(360),
            MinValueValidator(1)
        ]
    )
    lattitude = models.FloatField(
        default=0.0)
    longitude = models.FloatField(
        default = 0.0)
    uarfcn = models.IntegerField(
        default = 2937,
        validators=[
            MaxValueValidator(10838),
            MinValueValidator(412)
            ]
    )

class CompareCell(models.Model):
    cell_name = models.CharField(max_length=100)

class busyHourDaily(models.Model):
    startHour = models.IntegerField(
        default = 0,
        validators = [
            MaxValueValidator(23),
            MinValueValidator(0)
        ]
    )
    endHour = models.IntegerField(
        default =23,
        validators = [
            MaxValueValidator(23),
            MinValueValidator(0)
        ]
    )
    density = models.IntegerField(
    default = 99,
        validators = [
            MaxValueValidator(99),
            MinValueValidator(5)
        ]
    )
    busyHour = models.ForeignKey(CellInfo)
    def __unicode__(self):
        return str(self.busyHour)
