from django.utils import timezone
from rest_framework import serializers

from account.models import Account


class UserRegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'username', 'password', 'confirm_password']

    # confirm_email = serializers.SerializerMethodField()
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password = attrs.get("password")
        # Check clean password for password and confirm_password
        if password != attrs["confirm_password"]:
            error = serializers.ValidationError({"error": "The passwords do not match"})
            raise error
        return attrs

    def create(self, validated_data):
        email = validated_data.get("email")
        # raise an error if this email is already exists
        if Account.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "Email already registered"})
        user = Account.objects.create_user(
            password=validated_data["password"],
            email=validated_data["email"],
            username=email,
            is_active=False,
            last_login=timezone.now()
        )
        return user


class UserLoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'password']
