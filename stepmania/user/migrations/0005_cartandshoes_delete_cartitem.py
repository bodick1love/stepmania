# Generated by Django 5.0.1 on 2024-07-09 21:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0008_remove_cartitem_cart_remove_cartitem_shoes_and_more'),
        ('user', '0004_cart_cartitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartAndShoes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.cart')),
                ('shoes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.shoes')),
            ],
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]