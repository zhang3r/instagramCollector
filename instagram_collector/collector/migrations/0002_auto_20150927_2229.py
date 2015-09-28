# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pix',
            name='piclink',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='pix',
            name='tag',
            field=models.CharField(max_length=64),
        ),
    ]
