# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='persons',
            name='age',
            field=models.IntegerField(default=0, verbose_name='\u0412\u043e\u0437\u0440\u0430\u0441\u0442'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='persons',
            name='date_of_birth',
            field=models.DateField(verbose_name='\u0414\u0430\u0442\u0430 \u0440\u043e\u0436\u0434\u0435\u043d\u0438\u044f'),
        ),
        migrations.AlterField(
            model_name='persons',
            name='first_name',
            field=models.CharField(max_length=200, verbose_name='\u0418\u043c\u044f'),
        ),
        migrations.AlterField(
            model_name='persons',
            name='last_name',
            field=models.CharField(max_length=200, verbose_name='\u0424\u0430\u043c\u0438\u043b\u0438\u044f'),
        ),
        migrations.AlterField(
            model_name='persons',
            name='photo',
            field=models.CharField(max_length=200, verbose_name='\u041f\u0443\u0442\u044c \u043a \u0444\u043e\u0442\u043e'),
        ),
        migrations.AlterField(
            model_name='persons',
            name='votes',
            field=models.IntegerField(default=0, verbose_name='\u0420\u0435\u0439\u0442\u0438\u043d\u0433'),
        ),
    ]
