# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_auto_20150713_1245'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('color', models.CharField(default=b'red', max_length=50)),
                ('fontcolor', models.CharField(default=b'black', max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('color', models.CharField(default=b'red', max_length=50)),
                ('fontcolor', models.CharField(default=b'black', max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='note',
            name='location',
            field=models.ManyToManyField(related_name='notes', null=True, to='notes.Location', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='note',
            name='teacher',
            field=models.ManyToManyField(related_name='notes', null=True, to='notes.Teacher', blank=True),
            preserve_default=True,
        ),
    ]
