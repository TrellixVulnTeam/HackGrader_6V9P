# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('descrtiption', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ProblemTest',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('code', models.TextField()),
                ('extra_description', models.TextField()),
                ('language', models.ForeignKey(to='tester.Language')),
                ('problem', models.ForeignKey(to='tester.Problem')),
            ],
        ),
        migrations.CreateModel(
            name='RunResult',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('status', model_utils.fields.StatusField(choices=[('ok', 'ok'), ('not_ok', 'not_ok')], max_length=100, no_check_for_status=True, default='ok')),
                ('output', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TestRun',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created_at', models.DateField(auto_now=True)),
                ('status', model_utils.fields.StatusField(choices=[('pending', 'pending'), ('running', 'running'), ('done', 'done')], max_length=100, no_check_for_status=True, default='pending')),
                ('problem_test', models.ForeignKey(to='tester.ProblemTest')),
            ],
        ),
        migrations.AddField(
            model_name='runresult',
            name='run',
            field=models.ForeignKey(to='tester.TestRun'),
        ),
    ]
