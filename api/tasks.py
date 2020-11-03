from api.models import Shop
from api.serializers.update import CategoriesSerializer, ProductFileSerializer
from celery import shared_task
from django.db import transaction


@shared_task
def debug_task(request):
    return request

@shared_task
def update_from_file(data):
    category_serialyzer = CategoriesSerializer(
        data=data.get("categories"), many=True
    )
    for good in data.get("goods"):
        good["parameters"] = [
            {"name": name, "value": value}
            for name, value in good["parameters"].items()
        ]
    product_serilizer = ProductFileSerializer(
        data=data.get("goods"), many=True
    )
    # with transaction.atomic():
    shop = Shop.objects.get(name=data["shop"])
    category_serialyzer.is_valid(raise_exception=True)
    category_serialyzer.save()
        # with transaction.atomic():
    product_serilizer.is_valid(raise_exception=True)
    product_serilizer.save(shop=shop)