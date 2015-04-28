# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('recordId', models.AutoField(serialize=False, primary_key=True)),
                ('srNumber', models.BigIntegerField(null=True)),
                ('customer', models.CharField(max_length=1024, null=True)),
                ('description', models.TextField(null=True)),
                ('openDate', models.DateField(null=True)),
                ('modifiedDate', models.DateField(null=True)),
                ('touchDate', models.DateField(null=True)),
                ('closeDate', models.DateField(null=True)),
                ('escalationLevel', models.CharField(max_length=512, null=True)),
                ('calReviewDate', models.DateTimeField(null=True)),
                ('calSummary', models.TextField(null=True)),
                ('overallStatus', models.TextField(null=True)),
                ('reviewRequired', models.NullBooleanField(default=True)),
                ('calPriority', models.IntegerField(null=True)),
                ('faultCategory', models.TextField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
