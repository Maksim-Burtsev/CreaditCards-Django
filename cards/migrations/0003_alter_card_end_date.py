# Generated by Django 4.0.3 on 2022-03-15 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_alter_card_options_alter_card_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания активности'),
        ),
    ]
