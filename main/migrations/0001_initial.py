# Generated by Django 3.2 on 2021-04-24 04:24

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('name', models.CharField(default='UNNAMED', max_length=64)),
                ('name2', models.CharField(default='UNNAMED', max_length=64)),
                ('name3', models.CharField(default='UNNAMED', max_length=64)),
                ('score', models.IntegerField(default=0)),
                ('personal_info', models.CharField(default='NOINFO', max_length=64)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_accepted', models.BooleanField(default=False)),
                ('is_denied', models.BooleanField(default=False)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.student')),
            ],
        ),
    ]
