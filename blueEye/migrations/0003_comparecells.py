# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blueEye', '0002_auto_20151204_1258'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompareCells',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cell_name', models.CharField(max_length=100)),
            ],
        ),
    ]
