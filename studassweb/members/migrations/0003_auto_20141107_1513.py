# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_auto_20141107_1450'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentPurpose',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('purpose', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='payment',
            name='purpose',
            field=models.ForeignKey(to='members.PaymentPurpose'),
        ),
    ]
