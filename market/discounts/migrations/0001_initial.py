import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DiscountCart",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="наименование события")),
                ("percentage", models.PositiveIntegerField(default=0, verbose_name="процент скидки")),
                ("start_date", models.DateField(verbose_name="начало действия")),
                ("end_date", models.DateField(verbose_name="окончание действия")),
                (
                    "weight",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=3,
                        validators=[
                            django.core.validators.MinValueValidator(0.01),
                            django.core.validators.MaxValueValidator(1.0),
                        ],
                        verbose_name="вес скидки",
                    ),
                ),
                ("price_from", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="диапазон цены от")),
                ("price_to", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="диапазон цены до")),
            ],
            options={
                "verbose_name": "Скидка для корзины",
                "verbose_name_plural": "Скидки для корзины",
            },
        ),
        migrations.CreateModel(
            name="DiscountSet",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="наименование события")),
                ("percentage", models.PositiveIntegerField(default=0, verbose_name="процент скидки")),
                ("start_date", models.DateField(verbose_name="начало действия")),
                ("end_date", models.DateField(verbose_name="окончание действия")),
                (
                    "weight",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=3,
                        validators=[
                            django.core.validators.MinValueValidator(0.01),
                            django.core.validators.MaxValueValidator(1.0),
                        ],
                        verbose_name="вес скидки",
                    ),
                ),
                ("categories", models.ManyToManyField(related_name="discount_sets", to="products.category")),
            ],
            options={
                "verbose_name": "Скидка для набора",
                "verbose_name_plural": "Скидки на наборов",
            },
        ),
        migrations.CreateModel(
            name="DiscountProduct",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="наименование события")),
                ("percentage", models.PositiveIntegerField(default=0, verbose_name="процент скидки")),
                ("start_date", models.DateField(verbose_name="начало действия")),
                ("end_date", models.DateField(verbose_name="окончание действия")),
                ("products", models.ManyToManyField(related_name="discount_products", to="products.product")),
            ],
            options={
                "verbose_name": "Скидка для продукта",
                "verbose_name_plural": "Скидки для продуктов",
            },
        ),
    ]
