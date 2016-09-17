# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestWithBinaryFile',
            fields=[
                ('testrun_ptr', models.OneToOneField(to='tester.TestRun', primary_key=True, serialize=False, parent_link=True, auto_created=True)),
            ],
            bases=('tester.testrun',),
        ),
        migrations.CreateModel(
            name='TestWithPlainText',
            fields=[
                ('testrun_ptr', models.OneToOneField(to='tester.TestRun', primary_key=True, serialize=False, parent_link=True, auto_created=True)),
                ('solution_code', models.TextField()),
                ('test_code', models.TextField()),
            ],
            bases=('tester.testrun',),
        ),
    ]
