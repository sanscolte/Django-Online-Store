from typing import Any, Dict

from django.db.models import Avg, Subquery, OuterRef, CharField, Value, Count
from django.db.models.functions import Round, Concat
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.http import HttpRequest
from django.shortcuts import render, redirect  # noqa F401

from django.views.generic import ListView, DetailView
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django_filters.views import FilterView

from .models import Product, ProductDetail, ProductImage, ProductsViews
from .constants import KEY_FOR_CACHE_PRODUCTS
from .filters import ProductFilter
from .services.products_views_services import ProductsViewsService
from .services.reviews_services import ReviewsService
from .forms import ReviewForm, ProductDetailForm, ProductImageForm

from shops.models import Offer
from shops.forms import OfferForm


@method_decorator(cache_page(60 * 5, key_prefix=KEY_FOR_CACHE_PRODUCTS), name="dispatch")
class ProductListView(FilterView):
    template_name = "products/catalog.jinja2"
    context_object_name = "products"
    paginate_by = settings.PAGINATE_PRODUCTS_BY
    filterset_class = ProductFilter

    def get_queryset(self):
        images = ProductImage.objects.filter(product=OuterRef("pk")).order_by("sort_image")
        queryset = (
            Product.objects.annotate(reviews_count=Count("reviews"))
            .annotate(avg_price=Round(Avg("offers__price"), 2))
            .annotate(
                image=Concat(
                    Value(settings.MEDIA_URL),
                    Subquery(images.values("image")[:1]),
                    output_field=CharField(),
                ),
            )
            .order_by("date_of_publication")
        )
        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["query"] = dict()
        for k, v in context["filter"].data.items():
            if k != "page":
                context["query"][k] = v

        return context


@receiver([post_save, post_delete], sender=ProductDetail)
def clear_product_detail_cache(sender, instance, **kwargs):
    ProductDetailView.clear_cache_for_product_detail(instance.product.pk)


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.jinja2"
    context_object_name = "product"

    @staticmethod
    def get_cache_key(product_id):
        return f"product_detail_{str(product_id)}"

    @staticmethod
    def clear_cache_for_product_detail(product_id):
        cache.delete(ProductDetailView.get_cache_key(product_id))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cache_key = self.get_cache_key(self.object.pk)
        context["product_details"] = cache.get_or_set(
            cache_key, ProductDetail.objects.filter(product=self.object), settings.CACHE_TIME_DETAIL_PRODUCT_PAGE
        )

        review_service = ReviewsService(self.request, self.get_object())
        views_service = ProductsViewsService(self.get_object(), self.request.user)

        context["reviews"], context["next_page"], context["has_next"] = review_service.get_reviews_for_product()
        context["review_form"] = ReviewForm()
        context["reviews_count"] = review_service.get_reviews_count()
        context["product_details_form"] = ProductDetailForm()
        context["images"] = ProductImage.objects.filter(product=self.object)
        context["images_form"] = ProductImageForm()
        context["offers"] = Offer.objects.filter(product=self.object)
        context["offers_form"] = OfferForm()
        context["products_views"] = views_service.get_views()

        if self.request.user.is_authenticated:
            views_service.add_product_view()

        return context

    def post(self, request: HttpRequest, **kwargs):
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review_form.instance.user = self.request.user
            review_form.instance.product = self.get_object()
            review_form.save()

        return redirect(self.get_object())


class ProductsViewsView(ListView):
    model = ProductsViews
    template_name = "products/products-views.jinja2"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products_views"] = ProductsViews.objects.all()
        return context
