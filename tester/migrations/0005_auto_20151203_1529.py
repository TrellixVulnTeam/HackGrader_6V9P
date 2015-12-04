# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0004_auto_20151129_1903'),
    ]

    operations = [
        migrations.RenameField(
            model_name='problem',
            old_name='descrtiption',
            new_name='description',
        ),
    ]
