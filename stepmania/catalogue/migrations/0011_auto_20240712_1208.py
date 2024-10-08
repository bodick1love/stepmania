# Generated by Django 5.0.1 on 2024-07-12 09:08

from django.db import migrations
from django.db.models import F, Sum


def recalculate_order_price(apps, schema_editor):
    Order = apps.get_model('catalogue', 'Order')
    OrderAndShoes = apps.get_model('catalogue', 'OrderAndShoes')

    for order in Order.objects.all():
        shoes_price = OrderAndShoes.objects.filter(order=order).annotate(
            price=F('shoes__price')
        ).aggregate(
            val=Sum(F('price') * F('quantity'))
        )

        order.total_price = shoes_price['val'] + order.delivery_price or 0.0
        order.save()


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0010_order_total_price'),
    ]

    operations = [
        migrations.RunPython(recalculate_order_price)
    ]
