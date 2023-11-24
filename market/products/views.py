from django.shortcuts import render, redirect  # noqa F401

from django.views.generic import ListView, FormView
from django.conf import settings

from products.models import Product, Review
from .forms import ReviewForm


class ProductListView(ListView):
    template_name = "products/catalog.jinja2"
    model = Product
    context_object_name = "products"
    paginate_by = settings.PAGINATE_PRODUCTS_BY


class ProductDetailView(FormView):
    template_name = "products/product_detail.jinja2"
    form_class = ReviewForm
    success_url = "#"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.product = Product.objects.get(pk=self.kwargs.get("pk"))
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context["reviews"] = Review.objects.filter(product__pk=self.kwargs.get("pk"))
        context["product"] = Product.objects.get(pk=self.kwargs.get("pk"))
        return context
