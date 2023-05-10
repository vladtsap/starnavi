from rest_framework import serializers

from social_network.models import SocialUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = SocialUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = SocialUser
        fields = ('username', 'password')
