# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blueEye', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roundclock',
            old_name='hour1',
            new_name='hour',
        ),
    ]
