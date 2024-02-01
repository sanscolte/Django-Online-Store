from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    operations = [
        migrations.CreateModel(
            name="BankTransaction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("card_number", models.CharField(max_length=9)),
                ("total_price", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("is_success", models.BooleanField(null=True)),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="orders.order")),
            ],
            options={
                "verbose_name": "Оплата заказа",
                "verbose_name_plural": "Оплата заказов",
            },
        ),
    ]
