# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='body',
            field=models.TextField(blank=True, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='page',
            name='flags',
            field=models.IntegerField(choices=[(0, 'Normal page'), (1, 'Root page'), (2, 'Archive page')], default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='page',
            name='title',
            field=models.CharField(max_length=100, default=''),
            preserve_default=True,
        ),
    ]
