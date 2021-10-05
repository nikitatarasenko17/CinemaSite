from rest_framework import serializers
from django.db.models import Sum
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


    def validate(self, data):
        on_air = Sessions.objects.filter(hall_name=data['hall_name'])
        for i in on_air:
            if  i.start_session_time <= data['start_session_time'] <= i.end_session_time and \
                i.date_start_show <= data['date_start_show'] <= i.date_end_show or \
                i.start_session_time <= data['end_session_time'] <= i.end_session_time and \
                i.date_start_show <= data['date_end_show'] <= i.date_end_show:
                raise serializers.ValidationError('This hall doesnt exists')

        if data['start_session_time'] > data['end_session_time'] or data['date_start_show'] > data['date_end_show']:
            raise serializers.ValidationError('Session start cannot be greater than the end')
        return data    

class PurchaseSerializer(serializers.ModelSerializer):
    # session = SessionsSerializer()
    # quantity = serializers.IntegerField(required=True)
    # spent = serializers.SerializerMethodField()

    class Meta:
        model = Purchase
        fields = '__all__'
        # fields = ('id', 'spent', 'сonsumer', 'session', 'quantity')
        # read_only_fields = ('id', 'spent', 'сonsumer', )

    # def user_spent(self, obj):
    #     return obj.consumer.spent

    def validate(self, data):
        quantity = data['quantity']
        session = Sessions.objects.get(id=data['session'].id)
        user = MyUser.objects.get(id = self.context['request'].consumer_purchase.id)
        if (session.free_seats - quantity) < 0:
            raise serializers.ValidationError(f'Dont enough free seats!')
        session.free_seats -= quantity
        user.spent += quantity*session.price
        session.save()
        user.save()
        data['consumer'] = user
        return data