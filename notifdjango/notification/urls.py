from django.urls import path
from .views import home , addtogroup , NotificationCreateView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('' , home , name="home"),
    path('createnotification/' , NotificationCreateView.as_view() , name='create-notification'),
    path('addtogroup/<str:group_name>' , addtogroup , name="addtogroup"),
] \
+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)