from django.urls import path

from .views import IndexPageView, ShopDetailView

from config import settings
from django.conf.urls.static import static


app_name = "shops"


urlpatterns = [
    path("", IndexPageView.as_view(), name="home"),
    path("shops/<int:pk>/", ShopDetailView.as_view(), name="shops_detail"),
]

if settings.DEBUG:
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
