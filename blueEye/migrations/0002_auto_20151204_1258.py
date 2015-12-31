# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('blueEye', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cellinfo',
            name='uarfcn',
            field=models.IntegerField(default=2937, validators=[django.core.validators.MaxValueValidator(10838), django.core.validators.MinValueValidator(412)]),
        ),
        migrations.AlterField(
            model_name='cellinfo',
            name='azimuth',
            field=models.IntegerField(default=65, validators=[django.core.validators.MaxValueValidator(359), django.core.validators.MinValueValidator(0)]),
        ),
    ]
