# Generated by Django 3.2.6 on 2021-08-23 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_auto_20210823_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membershipfee',
            name='amount',
            field=models.PositiveIntegerField(default=200, verbose_name='Төлөм суммасы'),
        ),
    ]
