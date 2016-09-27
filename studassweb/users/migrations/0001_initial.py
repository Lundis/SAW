# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DummyPermissionBase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='KerberosLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='KerberosServer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('hostname', models.CharField(max_length=255, help_text='Example: domain.com, as in user@domain.com',
                                              unique=True)),
                ('realm', models.CharField(max_length=255, help_text='Example: SRV.DOMAIN.COM')),
                ('service', models.CharField(max_length=255, help_text='Example: krbtgt@SRV.DOMAIN.COM')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SAWPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=200)),
                ('module', models.CharField(max_length=100)),
                ('default_group', models.ForeignKey(default=None, null=True, to='auth.Group')),
                ('permission', models.ForeignKey(to='auth.Permission', unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserExtension',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('avatar', models.ImageField(default='users/avatars/default_avatar.png', upload_to='users/avatars')),
                ('description', models.TextField(blank=True, default='', max_length=1000)),
                ('link_to_homepage', models.URLField(blank=True, default='')),
                ('email_verified', models.BooleanField(default=False)),
                ('email_verification_code', models.CharField(max_length=32, unique=True)),
                ('incomplete', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
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
            unique_together={('server', 'username')},
        ),
    ]
