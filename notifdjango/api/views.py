from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import UserSerializer , RegisterSerializer
from rest_framework import permissions
from rest_framework.response import Response
from django.contrib.auth.models import User

class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer