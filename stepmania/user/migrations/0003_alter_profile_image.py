# Generated by Django 5.0.1 on 2024-07-02 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='user_images/default.png', upload_to='user_images'),
        ),
    ]