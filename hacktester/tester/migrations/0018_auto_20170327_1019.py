# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 10:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import hacktester.tester.models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0017_auto_20170327_1017'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=hacktester.tester.models.solutions_upload_path)),
                ('is_archive', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='testrun',
            name='solutions',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='run', to='tester.Solution'),
        ),
    ]
