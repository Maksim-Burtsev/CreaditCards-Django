# Generated by Django 4.0.2 on 2022-03-15 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0004_shopping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='release_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата выпуска'),
        ),
    ]