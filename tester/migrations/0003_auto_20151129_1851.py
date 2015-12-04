# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0002_testrun_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testrun',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
