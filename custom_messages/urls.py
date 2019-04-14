from rest_framework.routers import DefaultRouter
from .views import MessageViewSet

app_name = 'messages'

router = DefaultRouter()
router.register('messages', MessageViewSet, base_name='messages')


urlpatterns = [

]

urlpatterns += router.urls
