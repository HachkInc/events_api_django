from .models import Events, Tickets, User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'age', 'is_superuser', 'is_staff', 'email', 'password')


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ('id', 'title', 'login', 'password', 'address', 'time_start', 'time_end', 'max_guest_count',
                  'description')


class TicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = ('id', 'event_id', 'user_id', 'is_inside')


class QrSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'id')


class RegisterSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required = False)
    # first_name = serializers.CharField(required = False)
    # last_name = serializers.CharField(required = False)
    # age = serializers.IntegerField(required = False)
    # is_superuser = serializers.BooleanField(required=False)
    # is_staff = serializers.BooleanField(required= False)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        # fields = ('id', 'first_name', 'last_name', 'age', 'is_superuser', 'is_staff', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create(
            id = validated_data['id'],
            username=validated_data['email'],
            email=validated_data['email'],
            # is_superuser=validated_data['is_superuser'],
            # is_staff = validated_data['is_staff'],
            # first_name = validated_data['first_name'],
            # last_name=validated_data['last_name'],
            # age=validated_data['age']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user
