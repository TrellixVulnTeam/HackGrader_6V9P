# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import hacktester.tester.models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0007_testrun_extra_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchiveType',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('value', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
            ],
        ),
        migrations.AddField(
            model_name='testrun',
            name='number_of_results',
            field=models.IntegerField(default=1),
        ),
        migrations.CreateModel(
            name='ArchiveTest',
            fields=[
                ('test_ptr', models.OneToOneField(to='tester.Test', auto_created=True, serialize=False, primary_key=True, parent_link=True)),
                ('tests', models.FileField(upload_to=hacktester.tester.models.tests_upload_path)),
                ('archive_type', models.ForeignKey(to='tester.ArchiveType')),
            ],
            bases=('tester.test',),
        ),
        migrations.CreateModel(
            name='BinaryUnittest',
            fields=[
                ('test_ptr', models.OneToOneField(to='tester.Test', auto_created=True, serialize=False, primary_key=True, parent_link=True)),
                ('tests', models.FileField(upload_to=hacktester.tester.models.tests_upload_path)),
            ],
            bases=('tester.test',),
        ),
        migrations.CreateModel(
            name='PlainUnittest',
            fields=[
                ('test_ptr', models.OneToOneField(to='tester.Test', auto_created=True, serialize=False, primary_key=True, parent_link=True)),
                ('tests', models.TextField()),
            ],
            bases=('tester.test',),
        ),
    ]
