# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0005_auto_20160410_1454'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testwithbinaryfile',
            old_name='test',
            new_name='tests',
        ),
    ]
