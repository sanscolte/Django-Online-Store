from django.urls import path

from .views import MyLoginView
from config import settings
from django.conf.urls.static import static


app_name = "accounts"


urlpatterns = [
    path("login/", MyLoginView.as_view(), name="login"),
]

if settings.DEBUG:
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
