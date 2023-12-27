from rest_framework import routers
from .views import AccountViewSet, AccountRequestViewSet

router = routers.DefaultRouter()
router.register(r'accounts/requests', AccountRequestViewSet, 'request')
router.register(r'accounts', AccountViewSet, 'account')
urlpatterns = router.urls