# Generated by Django 5.0.4 on 2024-11-13 06:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_name', models.CharField(max_length=200)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='school_app.course')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('roll_number', models.CharField(max_length=10, unique=True)),
                ('date_of_birth', models.DateField()),
                ('is_approved', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('subjects', models.ManyToManyField(related_name='subjects', to='school_app.subject')),
            ],
        ),
    ]
