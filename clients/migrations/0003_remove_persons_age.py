# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_auto_20160407_2050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='persons',
            name='age',
        ),
    ]
