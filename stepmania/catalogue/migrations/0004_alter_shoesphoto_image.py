# Generated by Django 5.0.1 on 2024-06-20 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0003_shoesphoto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoesphoto',
            name='image',
            field=models.ImageField(upload_to='shoes_photo/'),
        ),
    ]
