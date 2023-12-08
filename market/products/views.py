from django.http import HttpRequest
from django.shortcuts import render, redirect  # noqa F401

from django.views.generic import ListView, DetailView
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache

from .models import Product, ProductDetail, ProductImage
from .constants import KEY_FOR_CACHE_PRODUCTS, KEY_FOR_CACHE_PRODUCT_DETAILS
from .services.reviews_services import ReviewsService
from .forms import ReviewForm, ProductDetailForm, ProductImageForm

from shops.models import Offer
from shops.forms import OfferForm


@method_decorator(cache_page(60 * 5, key_prefix=KEY_FOR_CACHE_PRODUCTS), name="dispatch")
class ProductListView(ListView):
    template_name = "products/catalog.jinja2"
    context_object_name = "products"
    model = Product
    paginate_by = settings.PAGINATE_PRODUCTS_BY


@method_decorator(cache_page(60 * 60 * 24, key_prefix=KEY_FOR_CACHE_PRODUCT_DETAILS), name="dispatch")
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
        context["product_details"] = ProductDetail.objects.filter(product=self.object)
        context["product_details_form"] = ProductDetailForm()
        context["images"] = ProductImage.objects.filter(product=self.object)
        context["images_form"] = ProductImageForm()
        context["offers"] = Offer.objects.filter(product=self.object)
        context["offers_form"] = OfferForm()
        return context

    def handle_product_details_update(self):
        # Логика обновления деталей товара
        # ...

        # Сброс кэша страницы товара
        cache_key = "product_page_cache" + str(self.object.pk)
        cache.delete(cache_key)

    def post(self, request: HttpRequest, **kwargs):
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review_form.instance.user = self.request.user
            review_form.instance.product = self.get_object()
            review_form.save()

        # Обработка POST-запроса, например, при обновлении деталей товара
        # ...
        # product_detail_form = ProductDetailForm(request.POST)
        # if product_detail_form.is_valid():
        #     product_detail_form.instance.product = self.get_object()
        #
        #     product_detail_form.save()
        #     self.handle_product_details_update()

        # return super().post(request, *args, **kwargs)

        return redirect(self.get_object())
