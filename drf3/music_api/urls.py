from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import SongViewSet, PlaylistViewSet

router = DefaultRouter()
router.register(r'songs', SongViewSet)
router.register(r'playlists', PlaylistViewSet)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/', include(router.urls)),
]