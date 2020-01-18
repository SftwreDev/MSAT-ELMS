from django.urls import path

from handouts import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'handouts'
urlpatterns = [
    path('list-of-handouts/', views.HandoutsList.as_view(), name='list-of-handouts'),
]

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
