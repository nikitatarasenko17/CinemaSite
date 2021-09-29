from rest_framework import serializers
from cinema.models import MyUser, Hall, Movies, Sessions, Purchase

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ['id', 'username', 'password' 'spent']

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = '__all__'        

class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'
        

class SessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sessions
        fields = '__all__'

class PurchaseSerializer(serializers.ModelSerializer):
    session = SessionsSerializer()

    class Meta:
        model = Purchase
        fields = '__all__'