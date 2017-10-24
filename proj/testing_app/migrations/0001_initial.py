# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-24 12:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_celery_results', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('set_number', models.IntegerField()),
                ('upload_date', models.DateTimeField(verbose_name='upload date')),
            ],
        ),
        migrations.CreateModel(
            name='SetValues',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value_a', models.IntegerField(verbose_name='value a')),
                ('value_b', models.IntegerField(verbose_name='value b')),
                ('set_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testing_app.DataSet')),
                ('task_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='django_celery_results.TaskResult')),
            ],
        ),
    ]