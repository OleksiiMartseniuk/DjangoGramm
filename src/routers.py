from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('src.account.urls')),
    path('authorization/', include('src.authorization.urls')),
    path('actions/', include('src.actions.urls')),
    path('social-auth/', include('social_django.urls',  namespace='social')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
