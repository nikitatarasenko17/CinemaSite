from django.db.models.base import Model
from cinema.models import MyUser
from cinema.API.autentification import TemporaryTokenAuthentication
from cinema.API.serializers import UserSerializer, HallSerializer, SessionsSerializer, PurchaseSerializer, MovieSerializer
from cinema.models import Hall, Movies, Sessions, Purchase, MyUser  
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.utils import timezone
from datetime import timedelta

class UserViewSet(ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer


class MovieViewSet(ModelViewSet):
    queryset = Movies.objects.all()
    serializer_class = MovieSerializer
    http_method_names = ['get', 'post', 'put', 'patch']
    

class HallViewSet(ModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    permission_classes = [IsAdminUser, ]
    http_method_names = ['get', 'post', 'put', 'patch']

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny, ]
        return super().get_permissions()    


class TodaySessionsViewSet(ModelViewSet):
    queryset = Sessions.objects.all()
    serializer_class = SessionsSerializer
    

    def get_queryset(self):
        today = timezone.now()
        return Sessions.objects.filter(date_start_show__lte = today, date_end_show__gt = today)

class TomorrowSessionsViewSet(ModelViewSet):
    queryset = Sessions.objects.all()
    serializer_class = SessionsSerializer

    def get_queryset(self):
        tomorrow = timezone.now() + timedelta(days=1)
        return Sessions.objects.filter(date_start_show__lte = tomorrow, date_end_show__gt = tomorrow)

class PurchaseViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        return self.request.user.consumer_purchase.all()    


