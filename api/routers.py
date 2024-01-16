"""Routes to the view"""

from rest_framework.routers import DefaultRouter

from apps.users.views import UserViewset


router = DefaultRouter()
router.register(r"user", UserViewset, basename="user")

urlpatterns = []
urlpatterns += router.urls
