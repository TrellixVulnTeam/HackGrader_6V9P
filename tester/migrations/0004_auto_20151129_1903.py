# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0003_auto_20151129_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testrun',
            name='status',
            field=model_utils.fields.StatusField(db_index=True, choices=[(0, 'dummy')], max_length=100, default='pending', no_check_for_status=True),
        ),
    ]
