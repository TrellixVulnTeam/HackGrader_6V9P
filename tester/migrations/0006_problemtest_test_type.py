# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0005_auto_20151203_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='problemtest',
            name='test_type',
            field=model_utils.fields.StatusField(db_index=True, default='unittest', choices=[(0, 'dummy')], max_length=100, no_check_for_status=True),
        ),
    ]
