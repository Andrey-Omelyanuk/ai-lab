from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('healthcheck'          , lambda request: JsonResponse({'status': 'OK'}), name='healthcheck'),
    path('admin/'               , admin.site.urls),
    path(''                     , lambda request: redirect('admin/')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG_TOOLBAR:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls')), ]

# if settings.SENTRY_ENDPOINT and settings.DEBUG:
#     def trigger_error(request):
#         division_by_zero = 1 / 0
#     urlpatterns += [path('sentry-debug/', trigger_error), ]
