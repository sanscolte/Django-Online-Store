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
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context["reviews"] = Review.objects.filter(product__pk=self.kwargs.get("pk"))
        context["form"] = ReviewForm()
        return context

    def post(self, request: HttpRequest, **kwargs):
        form = ReviewForm(request.POST)
        form.instance.user = self.request.user
        form.instance.product = Product.objects.get(pk=self.kwargs.get("pk"))

        if form.is_valid():
            form.save()
        else:
            form = ReviewForm()

        context = {
            "form": form,
            "reviews": Review.objects.filter(product__pk=self.kwargs.get("pk")),
            "product": Product.objects.get(pk=self.kwargs.get("pk")),
        }
        return render(request, "products/product_detail.jinja2", context)
