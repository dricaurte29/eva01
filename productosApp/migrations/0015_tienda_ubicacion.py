# Generated by Django 3.1.2 on 2020-12-28 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productosApp', '0014_auto_20201228_0056'),
    ]

    operations = [
        migrations.AddField(
            model_name='tienda',
            name='ubicacion',
            field=models.CharField(default=0, max_length=30),
            preserve_default=False,
        ),
    ]