# Generated by Django 3.1.2 on 2021-01-08 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productosApp', '0018_auto_20210107_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tienda',
            name='facebook_post',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='tienda',
            name='instagram_post',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
