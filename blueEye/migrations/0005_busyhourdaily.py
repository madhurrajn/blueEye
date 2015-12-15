# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('blueEye', '0004_auto_20151205_0738'),
    ]

    operations = [
        migrations.CreateModel(
            name='busyHourDaily',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('startHour', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(23), django.core.validators.MinValueValidator(0)])),
                ('endHour', models.IntegerField(default=23, validators=[django.core.validators.MaxValueValidator(23), django.core.validators.MinValueValidator(0)])),
                ('density', models.IntegerField(default=99, validators=[django.core.validators.MaxValueValidator(99), django.core.validators.MinValueValidator(5)])),
                ('busyHour', models.ForeignKey(to='blueEye.CellInfo')),
            ],
        ),
    ]
