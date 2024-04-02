# Generated by Django 5.0.1 on 2024-02-05 14:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0002_brand_category_alter_shoes_description_shoes_brand_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoesPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('shoes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.shoes')),
            ],
        ),
    ]
