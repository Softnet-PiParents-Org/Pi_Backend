# Generated by Django 5.1 on 2024-09-20 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_fee_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='count',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
    ]
