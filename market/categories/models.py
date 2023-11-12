from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """Категория"""

    name = models.CharField(max_length=512, verbose_name=_("наименование"), unique=True)
    description = models.TextField(verbose_name=_("описание"), blank=True)
    parent_id = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    sort_index = models.CharField(verbose_name=_("индекс сортировки"), blank=True)

    @property
    def description_short(self) -> str:
        if len(self.description) < 50:
            return self.description
        return self.description[:48] + "..."

    def __str__(self) -> str:
        return f"{self.name}"
