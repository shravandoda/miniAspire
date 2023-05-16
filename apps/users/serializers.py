# System
from datetime import timedelta

# Third Party
from django.contrib.auth import authenticate
from django.utils import timezone
from oauth2_provider.models import AccessToken, Application, RefreshToken
from oauthlib import common
from rest_framework import serializers

# App
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, allow_null=False)
    password = serializers.CharField(required=True, allow_null=False, write_only=True)
    first_name = serializers.CharField(required=True, allow_null=False)
    last_name = serializers.CharField(required=True, allow_null=False)
    email = serializers.CharField(required=True, allow_null=False)

    class Meta:
        model = User
        fields = ("id", "username", "password", "first_name", "last_name", "email")

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_null=False)
    password = serializers.CharField(required=True, allow_null=False, write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )
            if user:
                return {"user": user}
        raise serializers.ValidationError("Incorrect Credentials")

    def create(self, validated_data):
        user = validated_data["user"]
        application = Application.objects.first()

        # Create a new token for this user
        token_expiration = timezone.now() + timedelta(hours=1)
        access_token = AccessToken.objects.create(
            user=user,
            application=application,
            expires=token_expiration,
            scope="read write",
            token=common.generate_token(),
        )

        # Create a refresh_token for the corresponding access_token
        refresh_token = RefreshToken.objects.create(
            user=user,
            application=application,
            token=common.generate_token(),
            access_token=access_token,
        )

        return {
            "access_token": access_token.token,
            "expires_in": access_token.expires,
            "refresh_token": refresh_token.token,
            "token_type": "Bearer",
        }
