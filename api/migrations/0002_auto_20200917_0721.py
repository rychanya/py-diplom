# Generated by Django 3.1 on 2020-09-17 07:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="shop",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="productparameter",
            name="parameter",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.parameter"
            ),
        ),
        migrations.AddField(
            model_name="productparameter",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.product"
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="base",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.baseproduct"
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="parameters",
            field=models.ManyToManyField(
                through="api.ProductParameter", to="api.Parameter"
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="shop",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.shop"
            ),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.order"
            ),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.product"
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="cartitem",
            name="cart",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.cart"
            ),
        ),
        migrations.AddField(
            model_name="cartitem",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.product"
            ),
        ),
        migrations.AddField(
            model_name="cart",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="baseproduct",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.category"
            ),
        ),
    ]
