# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='busyHourDaily',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('startHour', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(23), django.core.validators.MinValueValidator(0)])),
                ('endHour', models.IntegerField(default=23, validators=[django.core.validators.MaxValueValidator(23), django.core.validators.MinValueValidator(0)])),
                ('density', models.IntegerField(default=99, validators=[django.core.validators.MaxValueValidator(99), django.core.validators.MinValueValidator(5)])),
            ],
        ),
        migrations.CreateModel(
            name='CellInfo',
            fields=[
                ('cell_name', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('azimuth', models.IntegerField(default=65, validators=[django.core.validators.MaxValueValidator(359), django.core.validators.MinValueValidator(0)])),
                ('radius', models.IntegerField(default=5, validators=[django.core.validators.MaxValueValidator(50), django.core.validators.MinValueValidator(1)])),
                ('beamwidth', models.IntegerField(default=65, validators=[django.core.validators.MaxValueValidator(360), django.core.validators.MinValueValidator(1)])),
                ('lattitude', models.FloatField(default=0.0)),
                ('longitude', models.FloatField(default=0.0)),
                ('uarfcn', models.IntegerField(default=2937, validators=[django.core.validators.MaxValueValidator(10838), django.core.validators.MinValueValidator(412)])),
            ],
        ),
        migrations.CreateModel(
            name='CompareCell',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cell_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='RoundClock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hour1', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(23), django.core.validators.MinValueValidator(0)])),
                ('density', models.IntegerField(default=99, validators=[django.core.validators.MaxValueValidator(99), django.core.validators.MinValueValidator(5)])),
                ('cell_name', models.CharField(default=b'default', max_length=99)),
            ],
        ),
        migrations.AddField(
            model_name='busyhourdaily',
            name='busyHour',
            field=models.ForeignKey(to='blueEye.CellInfo'),
        ),
    ]
