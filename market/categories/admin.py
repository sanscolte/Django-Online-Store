from django.contrib import admin

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "pk", "name", "description_short", "is_active"
    list_display_links = ("name",)
