from django.urls import include, path
from rest_framework import routers
from django.contrib import admin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from core.views import RegistroViewSet, UsuarioViewSet, LocalViewSet, produtividade_operadores, sum_all_working_hours, UsuarioProdutividadeView

router = routers.DefaultRouter()
router.register(r'locais', LocalViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'registros', RegistroViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('produtividade-operadores/', produtividade_operadores, name='produtividade_operadores'),  
    path('usuarios/<int:id>/produtividade/', UsuarioProdutividadeView.as_view(), name='usuario-produtividade'),
    path('totalhoras/', sum_all_working_hours, name='sum-all-working-hours'),
    path('', include(router.urls)),
]
