# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0006_auto_20160410_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='testrun',
            name='extra_options',
            field=jsonfield.fields.JSONField(blank=True, null=True),
        ),
    ]
