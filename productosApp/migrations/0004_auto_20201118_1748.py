# Generated by Django 3.1.2 on 2020-11-18 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productosApp', '0003_auto_20201109_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(null=True, upload_to='fotopr'),
        ),
    ]
