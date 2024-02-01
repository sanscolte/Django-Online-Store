from django.db import migrations, models
import django.db.models.deletion
import shops.utils


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Offer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("price", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="цена")),
                ("remains", models.IntegerField(default=0, verbose_name="остатки")),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="offers", to="products.product"
                    ),
                ),
            ],
            options={
                "verbose_name": "Предложение магазина",
                "verbose_name_plural": "Предложения магазина",
            },
        ),
        migrations.CreateModel(
            name="Shop",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=512, verbose_name="название")),
                ("description", models.CharField(max_length=1000, verbose_name="описание")),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=shops.utils.shop_preivew_directory_path,
                        verbose_name="изображение товара",
                    ),
                ),
                ("phone", models.CharField(max_length=128, verbose_name="телефон")),
                ("address", models.CharField(max_length=512, verbose_name="адрес")),
                ("email", models.EmailField(max_length=254, verbose_name="email")),
                (
                    "products",
                    models.ManyToManyField(
                        related_name="shops",
                        through="shops.Offer",
                        to="products.product",
                        verbose_name="товары в магазине",
                    ),
                ),
            ],
            options={
                "verbose_name": "Магазин",
                "verbose_name_plural": "Магазины",
            },
        ),
        migrations.AddField(
            model_name="offer",
            name="shop",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="offers", to="shops.shop"
            ),
        ),
        migrations.AddConstraint(
            model_name="offer",
            constraint=models.UniqueConstraint(models.F("shop"), models.F("product"), name="unique_product_in_shop"),
        ),
    ]
