# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nonce', models.BigIntegerField(db_index=True)),
                ('digest', models.CharField(max_length=64)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='apiuser',
            name='host',
            field=models.CharField(max_length=140, db_index=True),
        ),
        migrations.AlterField(
            model_name='apiuser',
            name='key',
            field=models.CharField(max_length=64, db_index=True),
        ),
        migrations.AddField(
            model_name='apirequest',
            name='user',
            field=models.ForeignKey(to='api_auth.ApiUser'),
        ),
    ]
