# Generated by Django 5.0.1 on 2024-07-10 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0009_orderandshoes_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.FloatField(default=1000),
        ),
    ]