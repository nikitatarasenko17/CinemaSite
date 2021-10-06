from django.db.models.base import Model
from cinema.models import MyUser
from cinema.API.autentification import TemporaryTokenAuthentication
from rest_framework.generics import RetrieveUpdateAPIView
from cinema.API.serializers import UserSerializer, HallSerializer, SessionsSerializer, PurchaseSerializer, MovieSerializer
# from cinema.API.permissions import SuperUserPermissionToSessionUpdate
from cinema.models import Hall, Movies, Sessions, Purchase, MyUser  
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from datetime import timedelta

class PersonalSetNumberPaginator(PageNumberPagination):
    page_size = 3


class UserViewSet(ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer


class MovieViewSet(ModelViewSet):
    queryset = Movies.objects.all()
    serializer_class = MovieSerializer
    http_method_names = ['get', 'post', 'put', 'patch']
    pagination_class = PersonalSetNumberPaginator

class HallViewSet(ModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    permission_classes = [IsAdminUser, ]
    pagination_class = PersonalSetNumberPaginator

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny, ]
        return super().get_permissions()    


class HallUpdateViewSet(RetrieveUpdateAPIView):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    permission_classes = [IsAdminUser, ]
    pagination_class = PersonalSetNumberPaginator


class CreateSessionsViewSet(ModelViewSet):
    queryset = Sessions.objects.all()
    serializer_class = SessionsSerializer
    pagination_class = PersonalSetNumberPaginator


class TodaySessionsViewSet(ModelViewSet):
    queryset = Sessions.objects.all()
    serializer_class = SessionsSerializer
    pagination_class = PersonalSetNumberPaginator
    
    def get_queryset(self):
        today = timezone.now()
        return Sessions.objects.filter(date_start_show__lte = today, date_end_show__gt = today)

class TomorrowSessionsViewSet(ModelViewSet):
    queryset = Sessions.objects.all()
    serializer_class = SessionsSerializer
    pagination_class = PersonalSetNumberPaginator

    def get_queryset(self):
        tomorrow = timezone.now() + timedelta(days=1)
        return Sessions.objects.filter(date_start_show__lte = tomorrow, date_end_show__gt = tomorrow)

class PurchaseViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    pagination_class = PersonalSetNumberPaginator

    def get_queryset(self):
        return self.request.user.consumer_purchase.all()    





