from typing import Any, Dict, Type

from django.db import ProgrammingError
from django.db.models import Avg, Subquery, OuterRef, CharField, Value, Count
from django.db.models.functions import Round, Concat
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.http import HttpRequest, HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404  # noqa F401
from django.views import View

from django.views.generic import ListView, DetailView
from django.conf import settings
from django_filters.views import FilterView

from accounts.models import User
from settings.models import SiteSetting
from .models import Product, ProductDetail, ProductImage, ProductsViews, ComparisonList
from .constants import KEY_FOR_CACHE_PRODUCTS
from .filters import ProductFilter
from .services.products_views_services import ProductsViewsService
from .services.reviews_services import ReviewsService
from .forms import ReviewForm, ProductDetailForm, ProductImageForm

from shops.models import Offer
from shops.forms import OfferForm
from cart.forms import CartAddProductForm
from cart.services import CartServices


def get_products_list_cache_time() -> int:
    """Lazy-функция для получения времени действия кэша каталога продуктов"""

    try:
        timeout = SiteSetting.objects.first().product_list_cache_time
    except (AttributeError, SiteSetting.DoesNotExist, ProgrammingError):
        timeout = settings.PRODUCT_LIST_CACHE_TIME
    return timeout


class ProductListView(FilterView):
    """Страница каталога товаров со средней ценой"""

    template_name = "products/catalog.jinja2"
    context_object_name = "products"
    paginate_by = settings.PAGINATE_PRODUCTS_BY
    filterset_class = ProductFilter

    def get_queryset(self):
        queryset = cache.get(KEY_FOR_CACHE_PRODUCTS)
        if queryset is not None:
            return queryset
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
        cache.set(KEY_FOR_CACHE_PRODUCTS, queryset)
        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["query"] = dict()
        context["cart_form"] = CartAddProductForm(initial={"quantity": 1, "update": False})
        for k, v in context["filter"].data.items():
            if k != "page":
                context["query"][k] = v

        return context

    def post(self, request: HttpRequest, **kwargs):
        cart_form = CartAddProductForm(request.POST)
        if cart_form.is_valid():
            product_name = request.POST["product_name"]
            product = Product.objects.get(name=product_name)
            quantity = cart_form.cleaned_data["quantity"]
            cart_services = CartServices(request)
            cart_services.add(
                product=product,
                shop=None,
                quantity=quantity,
                update_quantity=True,
            )
        return redirect("products:product-list")


class BaseComparisonView(View):
    """Базовое представление списка сравнения продуктов"""

    def get_comparison_list(self, request: HttpRequest) -> "ComparisonList":
        """Функция для получения списка сравнения"""

        comparison_list_id = request.session.get("comparison_list_id")

        if comparison_list_id:
            comparison_list = ComparisonList.objects.get(id=comparison_list_id)
        else:
            if request.user.is_authenticated:
                comparison_list = ComparisonList.objects.create(user=request.user)
            else:
                comparison_list = ComparisonList.objects.create(anonymous_user=True)
            request.session["comparison_list_id"] = comparison_list.id

        return comparison_list

    def get_comparison_count(self, request: HttpRequest, limit=3) -> int | bool:
        """Функция для получения количества продуктов в списке сравнения"""

        user_comparison_list = self.get_comparison_list(request)
        count = user_comparison_list.products.count()
        return count if count < limit else False

    def is_product_in_comparison(self, user: "User", product_id: int) -> int:
        """Функция для проверки наличия продукта в списке сравнения"""

        user_comparison_list = self.get_comparison_list(self.request)
        return product_id in user_comparison_list.products.values_list("id", flat=True)


class ComparisonListView(ListView, BaseComparisonView):
    """Представление списка сравнения продуктов"""

    model = ComparisonList
    template_name = "products/comparison-products.jinja2"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_comparison_list = self.get_comparison_list(self.request)

        comparison_products = user_comparison_list.products.all()
        products_views = ProductsViews.objects.filter(product__in=comparison_products)
        unique_details = ProductDetail.objects.filter(product__in=comparison_products)

        comparison_dict = {product.id: product for product in comparison_products}
        new_comparison_list = [comparison_dict[product_view.product.id] for product_view in products_views]

        context["products_in_comparison"] = new_comparison_list
        context["product_details_in_comparison"] = unique_details
        context["images"] = ProductImage.objects.filter(product__in=comparison_products)
        context["offers"] = Offer.objects.filter(product__in=comparison_products)
        context["cart_form"] = CartAddProductForm(initial={"quantity": 1, "update": False})

        return context

    def post(self, request: HttpRequest, **kwargs):
        cart_form = CartAddProductForm(request.POST)
        if cart_form.is_valid():
            product_name = request.POST["product_name"]
            product = Product.objects.get(name=product_name)
            quantity = cart_form.cleaned_data["quantity"]
            cart_services = CartServices(request)
            cart_services.add(
                product=product,
                shop=None,
                quantity=quantity,
                update_quantity=True,
            )
        return redirect("products:comparison-list")


@receiver([post_save, post_delete], sender=ProductDetail)
def clear_product_detail_cache(sender: Type[ProductDetail], instance: ProductDetail, **kwargs) -> None:
    """Функция очистки кэша характеристик продукта при получении сигналов post_save или post_delete"""

    ProductDetailView.clear_cache_for_product_detail(instance.product.pk)


class ProductDetailView(DetailView, BaseComparisonView):
    """Представление страницы характеристик продукта"""

    model = Product
    template_name = "products/product-details.jinja2"
    context_object_name = "product"

    @staticmethod
    def get_cache_key(product_id: int) -> str:
        """Функция для получения ключа кэша"""

        return f"product_detail_{str(product_id)}"

    @staticmethod
    def clear_cache_for_product_detail(product_id: int) -> None:
        """Функция для очистки кэша по ключу"""

        cache.delete(ProductDetailView.get_cache_key(product_id))

    def get_product_cache_time(self) -> int:
        """Lazy-функция для получения времени действия кэша характеристик продукта"""

        try:
            timeout = SiteSetting.objects.first().product_cache_time
        except (AttributeError, SiteSetting.DoesNotExist, ProgrammingError):
            timeout = settings.CACHE_TIME_DETAIL_PRODUCT_PAGE / 86400
        return timeout

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cache_key = self.get_cache_key(self.object.pk)
        context["product_details"] = cache.get_or_set(
            cache_key,
            ProductDetail.objects.filter(product=self.object),
            self.get_product_cache_time() * 86400,
        )

        review_service = ReviewsService(self.request, self.get_object())
        views_service = ProductsViewsService(self.get_object(), self.request.user)

        comparison_list = self.get_comparison_list(self.request)

        context["reviews"], context["next_page"], context["has_next"] = review_service.get_reviews_for_product()
        context["review_form"] = ReviewForm()
        context["cart_form"] = CartAddProductForm(initial={"quantity": 1, "update": False})
        context["reviews_count"] = review_service.get_reviews_count()
        context["product_details_form"] = ProductDetailForm()
        context["images"] = ProductImage.objects.filter(product=self.object)
        context["images_form"] = ProductImageForm()
        context["offers"] = Offer.objects.filter(product=self.object)
        context["offers_form"] = OfferForm()
        context["products_views"] = views_service.get_views()
        context["comparison_list"] = comparison_list
        context["is_product_in_comparison"] = self.is_product_in_comparison(self.request.user, self.object.pk)
        context["comparison_count"] = self.get_comparison_count(self.request)

        if self.request.user.is_authenticated:
            views_service.add_product_view()

        return context

    def post(self, request, **kwargs):
        action = request.POST.get("action")

        if action == "add_review":
            return self.handle_review(request)
        elif action == "add_to_cart":
            return self.handle_cart(request)
        else:
            return HttpResponseNotFound("Ошибка!")

    def handle_review(self, request: HttpRequest) -> HttpResponse:
        """Функция для обработки формы добавления отзыва в POST-методе"""

        review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            review_form.instance.user = self.request.user
            review_form.instance.product = self.get_object()
            review_form.save()
            return redirect("products:product-detail", pk=review_form.instance.product.pk)

        return HttpResponseNotFound("Ошибка!")

    def handle_cart(self, request: HttpRequest) -> HttpResponse:
        """Функция для обработки форма добавления товара в корзину в POST-методе"""

        cart_form = CartAddProductForm(request.POST)

        if cart_form.is_valid():
            shop_name = request.POST["shop_name"]
            quantity = cart_form.cleaned_data["quantity"]
            cart_services = CartServices(request)
            cart_services.add(
                product=self.get_object(),
                shop=shop_name,
                quantity=quantity,
                update_quantity=True,
            )
            return redirect(self.get_object())

        return HttpResponseNotFound("Ошибка!")


class AddToComparisonListView(ProductDetailView):
    """Представление добавления продукта в список сравнения продуктов"""

    def post(self, request, **kwargs):
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, id=product_id)
        user_comparison_list = self.get_comparison_list(request)
        if self.get_comparison_count(request) or not isinstance(self.get_comparison_count(request), bool):
            user_comparison_list.products.add(product)
        return redirect(self.get_object())


class RemoveFromComparisonListView(ProductDetailView):
    """Представление удаления продукта из списка сравнения продуктов"""

    def post(self, request, **kwargs):
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, id=product_id)
        user_comparison_list = self.get_comparison_list(request)
        user_comparison_list.products.remove(product)
        return redirect(self.get_object())


class ProductsViewsView(ListView):
    model = ProductsViews
    template_name = "products/products-views.jinja2"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products_views"] = ProductsViews.objects.all()
        return context
