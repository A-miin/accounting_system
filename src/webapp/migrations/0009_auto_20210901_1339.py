# Generated by Django 3.2.6 on 2021-09-01 07:39

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0008_auto_20210825_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='phone_number2',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Телефон 2'),
        ),
        migrations.AlterField(
            model_name='member',
            name='position',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Кызматы'),
        ),
        migrations.AlterField(
            model_name='member',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.region', verbose_name='Аймагы'),
        ),
        migrations.AlterField(
            model_name='member',
            name='village',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.village', verbose_name='Айылы'),
        ),
        migrations.AlterField(
            model_name='member',
            name='whatsapp_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Whatsapp номери'),
        ),
    ]
