# urls.py
from django.urls import include, path
from rest_framework import routers
from django.contrib import admin
from rest_framework_simplejwt.views import TokenRefreshView
from core.views import UserViewSet, RegistroViewSet, RegistroOpViewSet,  MyTokenObtainPairView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'registros', RegistroViewSet)
router.register(r'registroop', RegistroOpViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
