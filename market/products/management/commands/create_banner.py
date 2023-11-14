from django.core.management import BaseCommand

from products.models import Banner


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Create banner")

        for i in range(6):
            banner = Banner.objects.get_or_create(
                product_id=i,
                image="../static/img/content/home/slider.png",
                is_active=True,
            )

            self.stdout.write(self.style.SUCCESS(f"Created banner {banner}"))
