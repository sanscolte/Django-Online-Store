from django.contrib import admin
from .models import BankTransaction


@admin.register(BankTransaction)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "card_number",
        "total_price",
        "is_success",
    )
    list_display_links = ("order",)
