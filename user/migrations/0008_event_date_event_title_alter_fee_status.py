# Generated by Django 5.1 on 2024-09-21 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_fee_small_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='fee',
            name='status',
            field=models.CharField(choices=[('PAID', 'Paid'), ('UNPAID', 'Unpaid')], max_length=7),
        ),
    ]
