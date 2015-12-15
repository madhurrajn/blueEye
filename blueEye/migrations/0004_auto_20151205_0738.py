# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blueEye', '0003_comparecells'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CompareCells',
            new_name='CompareCell',
        ),
    ]
