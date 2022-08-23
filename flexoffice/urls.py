from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('flexoffice_app.urls')),
    path('twaask/', include('twaask_app.urls')),
    path('payment/', include('payment.urls')),
    path('admin/doc/', include('django.contrib.admindocs.urls'))


]

api_routes = [

    path('api/', include('flexoffice_app.routers')),
    path('api/', include('accounts.routers')),

]

urlpatterns += api_routes
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
            + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)