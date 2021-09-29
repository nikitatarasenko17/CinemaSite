from django.db.models.base import Model
from cinema.models import MyUser
from cinema.API.autentification import TemporaryTokenAuthentication
from cinema.API.serializers import UserSerializer, HallSerializer, SessionsSerializer, PurchaseSerializer, MovieSerializer
from cinema.models import Hall, Movies, Sessions, Purchase, MyUser  
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

class UserViewSet(ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer


class MovieViewSet(ModelViewSet):
    queryset = Movies.objects.all()
    serializer_class = MovieSerializer
    

class HallViewSet(ModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    permission_classes = [IsAdminUser, ]

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny, ]
        return super().get_permissions()    


class SessionsViewSet(ModelViewSet):
    queryset = Sessions.objects.all()
    serializer_class = SessionsSerializer


class PurchaseViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        return super().get_queryset().filter(consumer=self.request.user)    

    # def list(self, request, *args, **kwargs):
    #     queryset = Purchase.objects.filter(consumer=self.request.user)
    #     serializer = PurchaseSerializer(queryset, many=True)
    #     return Response(serializer.data)

