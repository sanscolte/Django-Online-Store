from django.db.models import Avg
from django.db.models.functions import Round
from django.http import HttpRequest
from django.shortcuts import render, redirect  # noqa F401

from django.views.generic import DetailView
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django_filters.views import FilterView

from products.models import Product
from .constants import KEY_FOR_CACHE_PRODUCTS
from .filters import ProductFilter
from .forms import ReviewForm
from .services.reviews_services import ReviewsService


@method_decorator(cache_page(60 * 5, key_prefix=KEY_FOR_CACHE_PRODUCTS), name="dispatch")
class ProductListView(FilterView):
    template_name = "products/catalog.jinja2"
    context_object_name = "products"
    paginate_by = settings.PAGINATE_PRODUCTS_BY
    filterset_class = ProductFilter

    def get_queryset(self):
        return Product.objects.annotate(avg_price=Round(Avg("offers__price"), 2))


class ProductDetailView(DetailView):
    template_name = "products/product_detail.jinja2"
    model = Product
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        review_service = ReviewsService(self.request, self.get_object())
        context["reviews"], context["next_page"], context["has_next"] = review_service.get_reviews_for_product()
        context["review_form"] = ReviewForm()
        context["reviews_count"] = review_service.get_reviews_count()
        return context

    def post(self, request: HttpRequest, **kwargs):
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review_form.instance.user = self.request.user
            review_form.instance.product = self.get_object()
            review_form.save()

        return redirect(self.get_object())
