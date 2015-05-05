# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recordlist', '0003_auto_20150505_0828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='calPriority',
            field=models.IntegerField(default=3),
            preserve_default=True,
        ),
    ]
