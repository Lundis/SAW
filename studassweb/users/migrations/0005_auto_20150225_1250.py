# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20150223_1444'),
    ]

    operations = [
        migrations.CreateModel(
            name='KerberosLink',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('username', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='KerberosServer',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('hostname', models.CharField(unique=True, max_length=255, help_text='Example: domain.com, as in user@domain.com')),
                ('realm', models.CharField(max_length=255, help_text='Example: srv.domain.com')),
                ('service', models.CharField(max_length=255, help_text='Example: krbtgt@srv.domain.com')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='ldaplink',
            name='user',
        ),
        migrations.DeleteModel(
            name='LdapLink',
        ),
        migrations.AddField(
            model_name='kerberoslink',
            name='server',
            field=models.ForeignKey(to='users.KerberosServer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='kerberoslink',
            name='user',
            field=models.ForeignKey(to='users.UserExtension'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='kerberoslink',
            unique_together=set([('server', 'username')]),
        ),
    ]
