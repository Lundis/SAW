# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import base.fields
from django.conf import settings
import events.models
import django.core.validators


class Migration(migrations.Migration):

    replaces = [('events', '0001_initial'), ('events', '0002_auto_20150204_1339'), ('events', '0003_auto_20150204_1417'), ('events', '0004_eventsignup_delete_confirmation_code'), ('events', '0005_auto_20150210_1937'), ('events', '0006_auto_20150211_0025'), ('events', '0007_auto_20150211_1422'), ('events', '0008_remove_iteminsignup_amount'), ('events', '0009_auto_20150211_1813'), ('events', '0010_auto_20150211_2108'), ('events', '0011_auto_20150212_1404'), ('events', '0012_auto_20150212_1808'), ('events', '0013_auto_20150212_1824'), ('events', '0014_auto_20150212_1839'), ('events', '0015_event_max_participants'), ('events', '0016_event_signup_start'), ('events', '0017_auto_20150213_1217'), ('events', '0018_auto_20150213_1245'), ('events', '0019_eventsignup_order_id'), ('events', '0020_auto_20150220_1107'), ('events', '0021_auto_20150221_1620'), ('events', '0022_auto_20150223_1322'), ('events', '0023_auto_20150226_1927'), ('events', '0024_eventsettings')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('text', models.TextField(max_length=500)),
                ('start', models.DateTimeField()),
                ('stop', models.DateTimeField()),
                ('signup_deadline', models.DateTimeField()),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventItem',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventSignup',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=75)),
                ('matricle', models.CharField(max_length=20)),
                ('association', models.CharField(max_length=200)),
                ('diet', models.CharField(max_length=200)),
                ('other', models.CharField(max_length=200)),
                ('event', models.ForeignKey(to='events.Event')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemInEvent',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('event', models.ForeignKey(to='events.Event')),
                ('item', models.ForeignKey(to='events.EventItem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemInSignup',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('item', models.ForeignKey(to='events.EventItem')),
                ('signup', models.ForeignKey(to='events.EventSignup')),
                ('value', events.models.MultiInputField(null=True, blank=True, max_length=500)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='eventsignup',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='eventsignup',
            name='diet',
        ),
        migrations.RemoveField(
            model_name='eventsignup',
            name='other',
        ),
        migrations.AlterField(
            model_name='eventsignup',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventsignup',
            name='auth_code',
            field=models.CharField(default='', unique=True, max_length=32),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='permission',
            field=models.CharField(choices=[('can_view_and_join_public_events', 'Public event'), ('can_view_and_join_member_events', 'Members-only event'), ('can_view_and_join_board_member_events', 'Board members-only event')], default='can_view_and_join_public_events', max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='slug',
            field=models.SlugField(default='aaa', unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventitem',
            name='required',
            field=models.BooleanField(verbose_name='Is this field mandatory', default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventitem',
            name='type',
            field=models.CharField(max_length=1, choices=[('B', 'Checkbox'), ('S', 'Text (one line)'), ('T', 'Text (multiple lines)'), ('I', 'Integer'), ('C', 'Choice')], verbose_name='Data type', help_text='Decides what kind of data is allowed in this field. The options are:<br />Checkbox: A simple checkbox (yes/no)<br />Text (one line): A text field with one line <br />Text (multiple lines): A larger resizeable text field that allows multiple lines<br />Integer: A number<br />Choice: A multiple-choices field. syntax for name: question//alternative1//alternative2//alternative3', default='I'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='eventsignup',
            name='association',
        ),
        migrations.RemoveField(
            model_name='eventsignup',
            name='matricle',
        ),
        migrations.AlterField(
            model_name='event',
            name='text',
            field=base.fields.ValidatedRichTextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='signup_deadline',
            field=models.DateTimeField(verbose_name='Deadline for signups'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='start',
            field=models.DateTimeField(verbose_name='Event ends'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='stop',
            field=models.DateTimeField(verbose_name='Event starts'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='text',
            field=base.fields.ValidatedRichTextField(verbose_name='Description'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='eventsignup',
            name='name',
            field=models.CharField(verbose_name='Full name', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterModelOptions(
            name='eventsignup',
            options={'ordering': ('created',)},
        ),
        migrations.AddField(
            model_name='event',
            name='max_participants',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], default=50),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='signup_start',
            field=models.DateTimeField(verbose_name='Signup starts', default=django.utils.timezone.now),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventsignup',
            name='order_id',
            field=models.IntegerField(validators=django.core.validators.MinValueValidator(1), default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventitem',
            name='hide_in_print_view',
            field=models.BooleanField(verbose_name='Is this field hidden from the print view?', default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventitem',
            name='public',
            field=models.BooleanField(verbose_name='Is this field shown to everyone?', default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='send_email_for_reserves',
            field=models.BooleanField(verbose_name='Send email when someone is moved from reserve list to attending', default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='use_captcha',
            field=models.BooleanField(verbose_name='Use captcha when anonymous people sign up', default=False),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='EventSettings',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('is_setup', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
