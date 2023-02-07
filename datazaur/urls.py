
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls'), name='website'),
    path('markets/', include('markets.urls'), name='markets'),
    path('crypto/', include('crypto.urls'), name='crypto'),
    path('monitor/', include('monitor.urls'), name='monitor'),
    path('macro/', include('macro.urls'), name='macro'),
    path('companies/', include('companies.urls'), name='companies'),
    path('calendar/', include('calendar_.urls'), name='calendar'),
    path('news/', include('news.urls'), name='news'),
    path('api/', include('api.urls'), name='api'),

]



