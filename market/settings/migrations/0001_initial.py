import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SiteSetting",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(default="Настройка сайта")),
                (
                    "min_order_price_for_free_shipping",
                    models.DecimalField(
                        decimal_places=2,
                        default=2000.0,
                        max_digits=6,
                        verbose_name="minimum order price for free shipping, $",
                    ),
                ),
                (
                    "standard_order_price",
                    models.DecimalField(
                        decimal_places=2, default=200.0, max_digits=6, verbose_name="standard order price, $"
                    ),
                ),
                (
                    "express_order_price",
                    models.DecimalField(
                        decimal_places=2, default=500.0, max_digits=6, verbose_name="express order price, $"
                    ),
                ),
                (
                    "banners_count",
                    models.PositiveIntegerField(
                        default=3,
                        validators=[django.core.validators.MaxValueValidator(3)],
                        verbose_name="banners count",
                    ),
                ),
                ("days_offer", models.BooleanField(default=True, verbose_name="show days offer")),
                (
                    "top_items_count",
                    models.PositiveIntegerField(
                        default=8,
                        validators=[django.core.validators.MaxValueValidator(8)],
                        verbose_name="top items count",
                    ),
                ),
                (
                    "limited_edition_count",
                    models.PositiveIntegerField(
                        default=16,
                        validators=[django.core.validators.MaxValueValidator(16)],
                        verbose_name="limited edition count",
                    ),
                ),
                (
                    "product_cache_time",
                    models.PositiveIntegerField(default=1.0, verbose_name="product cache time, days"),
                ),
                ("banner_cache_time", models.PositiveIntegerField(default=600, verbose_name="banner cache time")),
                (
                    "product_list_cache_time",
                    models.PositiveIntegerField(default=300, verbose_name="product list cache time"),
                ),
            ],
            options={
                "verbose_name": "настройка",
                "verbose_name_plural": "настройки",
            },
        ),
    ]
