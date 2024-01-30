"""Routes to the view"""

from rest_framework.routers import DefaultRouter

from django.conf.urls.static import static
from django.conf import settings

from apps.users.views import UserViewset
from apps.artisans.views import ArtisanViewset


router = DefaultRouter()
router.register(r"user", UserViewset, basename="user")
router.register(r"artisan", ArtisanViewset, basename="artisan")

urlpatterns = []
urlpatterns += router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)