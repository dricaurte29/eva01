# Generated by Django 3.1.2 on 2020-12-28 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productosApp', '0013_auto_20201228_0045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='imagen2',
            field=models.ImageField(blank=True, upload_to='fotopr'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='imagen3',
            field=models.ImageField(blank=True, upload_to='fotopr'),
        ),
    ]
