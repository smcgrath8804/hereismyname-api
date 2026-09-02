from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from . import views
from django.urls import path, include
from drf_spectacular.views import (SpectacularAPIView, SpectacularSwaggerView,)


urlpatterns = [
    ## ==== Home ====
    path("", views.home, name="home"),

    ## ==== Admin ====
    path('admin/', admin.site.urls),

    ## ==== Website pages ====
    path("users/", include("users.urls")),
    path("profiles/", include("profiles.urls")),
    path("connections/", include("connections.urls")),
    path("visibility/", include("visibility.urls")),
    path("links/", include("links.urls")),

    ## ==== API documentation ====
    path('api/schema/', SpectacularAPIView.as_view(), name='schema',),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui',),

    ## ==== API routes ====
    path("api/", include("api.urls")),
]

## Serve uploaded media files during development
## Source: https://docs.djangoproject.com/en/6.0/howto/static-files/#serving-files-uploaded-by-a-user-during-development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )