from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["offer"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "full_name",
        "email",
        "phone_number",
        "created_at",
        "delivery_type",
        "address",
        "city",
        "payment_type",
        "status",
        "total_price",
    ]
    list_filter = ["created_at"]
    inlines = [OrderItemInline]
