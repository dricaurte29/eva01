# Generated by Django 3.1.2 on 2020-11-21 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productosApp', '0006_pedido_local'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='contacto',
            field=models.IntegerField(default=300),
            preserve_default=False,
        ),
    ]
