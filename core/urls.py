from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view
from django.conf import settings
from django.conf.urls.static import static

app_name = 'core'

schema_view = get_swagger_view(title='API Docs')


urlpatterns = [
    url(r'^docs/', schema_view),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
