# Generated by Django 5.0.1 on 2024-07-08 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0004_alter_shoesphoto_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.CharField(choices=[('Cash', 'Card')], default='Cash', max_length=4),
        ),
    ]
