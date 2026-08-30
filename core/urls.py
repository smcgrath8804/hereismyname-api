from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from . import views
from django.urls import path, include
from drf_spectacular.views import (SpectacularAPIView, SpectacularSwaggerView,)


urlpatterns = [
    path("", views.home, name="home"),
    path('admin/', admin.site.urls),
    path("users/", include("users.urls")),
    path('api/schema/',
        SpectacularAPIView.as_view(),
        name='schema',
    ),
    path('api/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path("profiles/", include("profiles.urls")),
    path("connections/", include("connections.urls")),
    path("visibility/", include("visibility.urls")),
    path("api/", include("api.urls")),
    path("links/", include("links.urls"),
    ),
]
## Source: https://docs.djangoproject.com/en/6.0/howto/static-files/#serving-files-uploaded-by-a-user-during-development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )