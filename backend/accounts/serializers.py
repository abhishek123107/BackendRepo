from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'is_staff', 'is_superuser', 'date_joined', 'is_active'
        ]
        read_only_fields = ['id', 'date_joined', 'is_staff', 'is_superuser']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=6,
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate_password(self, value):
        """Custom password validation - more lenient than Django's default"""
        if len(value) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters long.")
        
        # Allow numeric passwords but require minimum length
        if value.isdigit() and len(value) < 8:
            raise serializers.ValidationError("Numeric passwords must be at least 8 characters long.")
        
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password2": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user