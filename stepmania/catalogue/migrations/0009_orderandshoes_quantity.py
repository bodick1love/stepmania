# Generated by Django 5.0.1 on 2024-07-10 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0008_remove_cartitem_cart_remove_cartitem_shoes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderandshoes',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
