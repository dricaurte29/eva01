# Generated by Django 3.1.2 on 2021-01-17 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productosApp', '0022_producto_estatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='puntuacion',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producto',
            name='nr',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producto',
            name='tr',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]