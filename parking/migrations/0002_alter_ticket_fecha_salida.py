# Generated by Django 4.1.5 on 2023-01-19 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='fecha_salida',
            field=models.DateTimeField(null=True),
        ),
    ]
