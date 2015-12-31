# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blueEye', '0005_busyhourdaily'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cellinfo',
            name='id',
        ),
        migrations.AlterField(
            model_name='cellinfo',
            name='cell_name',
            field=models.CharField(max_length=100, serialize=False, primary_key=True),
        ),
    ]
