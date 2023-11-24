from django.http import HttpRequest
from django.shortcuts import render, redirect  # noqa F401

from django.views.generic import ListView, DetailView
from django.conf import settings

from products.models import Product, Review
from .forms import ReviewForm


class ProductListView(ListView):
    template_name = "products/catalog.jinja2"
    model = Product
    context_object_name = "products"
    paginate_by = settings.PAGINATE_PRODUCTS_BY


class ProductDetailView(DetailView):
    template_name = "products/product_detail.jinja2"
    model = Product
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = Review.objects.filter(product=self.object)
        context["form"] = ReviewForm()  # FIXME переименовать ключ в review_form, т.к. на странице будут и другие формы
        return context

    def post(self, request: HttpRequest, **kwargs):
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.instance.user = self.request.user
            form.instance.product = self.get_object()
            form.save()

        return redirect(self.get_object())
