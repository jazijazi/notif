from django.urls import path,include
from rest_framework import routers
from .views import CurrentUserView , RegisterView



app_name = "api"

router = routers.SimpleRouter()
#router.register('user/current/' , CurrentUserView , basename="currentuser")

urlpatterns = [
    path("" , include(router.urls)),
    path('user/current/' , CurrentUserView.as_view() , name="currentuser"),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
]
