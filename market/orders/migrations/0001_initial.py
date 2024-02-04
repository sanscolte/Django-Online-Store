from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("shops", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=50, verbose_name="полное имя")),
                ("email", models.EmailField(max_length=254, verbose_name="email")),
                ("phone_number", models.CharField(max_length=12, verbose_name="телефон")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="создан")),
                (
                    "delivery_type",
                    models.CharField(
                        choices=[("regular", "обычная доставка"), ("express", "экспресс-доставка")],
                        default="regular",
                        max_length=50,
                        verbose_name="доставка",
                    ),
                ),
                ("address", models.CharField(max_length=250, verbose_name="адрес")),
                ("city", models.CharField(max_length=50, verbose_name="город")),
                (
                    "payment_type",
                    models.CharField(
                        choices=[("card", "онлайн картой"), ("random", "онлайн со случайного чужого счета")],
                        default="card",
                        max_length=50,
                        verbose_name="оплата",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("created", "Status Created"),
                            ("ok", "Status Ok"),
                            ("delivered", "Status Delivered"),
                            ("paid", "Status Paid"),
                            ("not paid", "Status Not Paid"),
                        ],
                        default="created",
                        max_length=15,
                        verbose_name="статус",
                    ),
                ),
                (
                    "total_price",
                    models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name="итоговая цена"),
                ),
            ],
            options={
                "verbose_name": "Заказ",
                "verbose_name_plural": "Заказы",
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("price", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="цена")),
                ("quantity", models.PositiveIntegerField(default=1, verbose_name="количество")),
                (
                    "offer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_items",
                        to="shops.offer",
                        verbose_name="предложение",
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="orders.order",
                        verbose_name="заказ",
                    ),
                ),
            ],
            options={
                "verbose_name": "Продукты в Заказе",
                "verbose_name_plural": "Продукты в Заказе",
            },
        ),
    ]
