# Generated by Django 3.1.2 on 2020-12-28 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productosApp', '0008_producto_categorian'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='imagen',
        ),
        migrations.AddField(
            model_name='producto',
            name='imagen1',
            field=models.ImageField(default=0, upload_to='fotopr'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producto',
            name='imagen2',
            field=models.ImageField(null=True, upload_to='fotopr'),
        ),
        migrations.AddField(
            model_name='producto',
            name='imagen3',
            field=models.ImageField(null=True, upload_to='fotopr'),
        ),
    ]
