# Generated by Django 5.0.4 on 2024-11-14 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_app', '0003_question_choice'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]
