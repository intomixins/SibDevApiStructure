# Generated by Django 4.2.5 on 2023-09-13 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='count_gems',
            field=models.CharField(default='', max_length=455),
        ),
    ]