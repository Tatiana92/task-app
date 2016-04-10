# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_remove_persons_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='persons',
            name='age',
            field=models.IntegerField(default=0, verbose_name='\u0412\u043e\u0437\u0440\u0430\u0441\u0442'),
            preserve_default=True,
        ),
    ]
