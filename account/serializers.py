from djoser.serializers import UserSerializer
from rest_framework import serializers
from .models import CustomUser, UserInfo, BookingHistory

class Userserializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = '__all__'


class Userinfoserializer(serializers.ModelSerializer):
    userid = serializers.UUIDField(read_only = True)
    class Meta:
        model = UserInfo
        fields = '__all__'

class Bookinghistoryserializer(serializers.ModelSerializer):
    historyid = serializers.UUIDField(read_only = True)
    class Meta:
        model = BookingHistory
        fields = '__all__'

class AuthorizationTokenSerializer(serializers.Serializer):
    account = serializers.HyperlinkedRelatedField(
        queryset=CustomUser.objects.all(),
        required=True,
        view_name='api:account-detail',
)

    class Meta:
        fields = ['account']