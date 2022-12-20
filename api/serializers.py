from .models import Events, Tickets, CustomUser
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
#   "first_name": "string",
#   "last_name": "string",
#   "age": 0,
#   "qr_code": "string",
#   "is_superuser": true,
#   "is_staff": true,
#   "email": "user@example.com",
#   "password": "123123",
#   "username": "daniil",

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # fields = ('id', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'email', 'password')
        fields = ('first_name', 'last_name', 'email', 'password', 'age', 'qr_code', 'username')
        # fields = '__all__'

class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ('id', 'title', 'login', 'password', 'address', 'time_start', 'time_end', 'max_guest_count',
                  'description')


class TicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = ('id', 'event_id', 'user_id', 'is_inside')


class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required = False)
    last_name = serializers.CharField(required = False)
    age = serializers.IntegerField(required = False)
    qr_code = serializers.CharField(required = False)
    is_superuser = serializers.BooleanField(required=False)
    is_staff = serializers.BooleanField(required= False)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        # fields = ('first_name', 'last_name', 'is_superuser', 'is_staff', 'email', 'password')
        # fields = '__all__'
        fields = ('first_name', 'last_name', 'email', 'password', 'age','qr_code' , 'is_superuser', 'is_staff', 'username')
    # def validate(self, attrs):
    #     if attrs['password'] != attrs['password2']:
    #         raise serializers.ValidationError(
    #             {"password": "Password fields didn't match."})
    #     return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            age=validated_data['age'],
            qr_code=validated_data['qr_code']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user
