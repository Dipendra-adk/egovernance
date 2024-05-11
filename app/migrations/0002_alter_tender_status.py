# Generated by Django 5.0.4 on 2024-05-07 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tender',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Active', 'Active'), ('Closed', 'Closed')], default='Pending', max_length=7),
        ),
    ]