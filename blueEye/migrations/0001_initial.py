# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CellInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cell_name', models.CharField(max_length=100)),
                ('azimuth', models.IntegerField(default=65, validators=[django.core.validators.MaxValueValidator(360), django.core.validators.MinValueValidator(1)])),
                ('radius', models.IntegerField(default=5, validators=[django.core.validators.MaxValueValidator(50), django.core.validators.MinValueValidator(1)])),
                ('beamwidth', models.IntegerField(default=65, validators=[django.core.validators.MaxValueValidator(360), django.core.validators.MinValueValidator(1)])),
                ('lattitude', models.FloatField(default=0.0)),
                ('longitude', models.FloatField(default=0.0)),
            ],
        ),
    ]
