# Generated by Django 3.1 on 2020-08-25 23:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_cartitem_cart"),
    ]

    operations = [
        migrations.AddField(
            model_name="shop",
            name="delivery_price",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="cartitem",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.product"
            ),
        ),
    ]
