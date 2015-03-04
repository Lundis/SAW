# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [('users', '0001_initial'), ('users', '0002_sawpermission_default_group'), ('users', '0003_sawpermission_module'), ('users', '0004_auto_20150223_1444'), ('users', '0005_auto_20150225_1250'), ('users', '0006_userextension_incomplete'), ('users', '0007_auto_20150304_2145')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DummyPermissionBase',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SAWPermission',
            fields=[
                ('permission', models.ForeignKey(unique=True, to='auth.Permission')),
                ('description', models.CharField(max_length=200)),
                ('default_group', models.ForeignKey(default=None, to='auth.Group', null=True)),
                ('module', models.CharField(default='unset (run install!!)', max_length=100)),
                ('id', models.AutoField(default=None, serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserExtension',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('avatar', models.ImageField(default='users/avatars/default_avatar.png', upload_to='users/avatars')),
                ('description', models.TextField(blank=True, default='', max_length=1000)),
                ('link_to_homepage', models.URLField(blank=True, default='')),
                ('email_verified', models.BooleanField(default=False)),
                ('email_verification_code', models.CharField(unique=True, max_length=32)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('incomplete', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='KerberosLink',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='KerberosServer',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('hostname', models.CharField(unique=True, max_length=255, help_text='Example: domain.com, as in user@domain.com')),
                ('realm', models.CharField(max_length=255, help_text='Example: SRV.DOMAIN.COM')),
                ('service', models.CharField(max_length=255, help_text='Example: krbtgt@SRV.DOMAIN.COM')),
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
            unique_together=set([('server', 'username')]),
        ),
    ]
