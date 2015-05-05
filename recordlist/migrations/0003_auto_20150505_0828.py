# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recordlist', '0002_auto_20150505_0817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='calPriority',
            field=models.IntegerField(default=3, null=True),
            preserve_default=True,
        ),
    ]
