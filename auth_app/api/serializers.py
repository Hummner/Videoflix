from rest_framework import serializers
from django.contrib.auth.models import User
import random
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    - Requires `password` + `confirmed_password`.
    - Generates a unique username automatically from the email (with a random suffix).
    - Creates the user as inactive (activation happens via email token flow).
    """
    confirmed_password = serializers.CharField(write_only=True)
    username = serializers.CharField(read_only=True)

    def validate(self, attrs):
        """Ensure password and confirmed_password match."""
        password = attrs.get('password')
        confirmed_password = attrs.get('confirmed_password')

        if password != confirmed_password:
            raise serializers.ValidationError('Password and confirmation do not match.')

        return attrs
    
    def create(self, validated_data):
        """
        Create a new inactive user.

        - Removes confirmed_password from validated_data.
        - Generates a unique username.
        """
        validated_data.pop('confirmed_password')
        email = validated_data['email']
        username = self.generate_unique_username(email)

        user = User.objects.create(username=username, **validated_data)
        user.is_active=False
        user.save()
        return user


    def generate_unique_username(self, email):
        """
        Generate a unique username based on the email prefix.

        Example:
        - email: john@example.com
        - username: john#1234
        """
        base_username = email.split('@')[0]

        while True:
            suffix = random.randint(1000, 9999)
            username = f"{base_username}#{suffix}"
            if not User.objects.filter(username=username).exists():
                return username


    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'confirmed_password']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT login serializer that authenticates via email instead of username.

    - Accepts: email + password
    - Internally maps email -> username and delegates token generation to SimpleJWT.
    """
    email = serializers.EmailField()

    def __init__(self, *args, **kwargs):
        """Remove the default username field and use email instead."""
        super().__init__(*args, **kwargs)
        if "username" in self.fields:
            self.fields.pop('username')
     
    
    def validate(self, attrs):
        """
        Validate credentials.

        - Finds the user by email.
        - If found, passes username + password to the base SimpleJWT logic.
        """
        email = attrs['email']
        password = attrs['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'error': 'Email or password is wrong'})
        
        data = super().validate({
            "username":user.username,
            "password":password
            }
        )
    
        return data
    

class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset.

    - Validates the email field.
    - If a user exists, attaches the user object to validated data (attrs['user']).
    """
    email = serializers.EmailField()

    def validate(self, attrs):
        """Attach the user to attrs if the email exists."""
        email = attrs['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return attrs
        
        attrs['user']=user

        return attrs
    

class ConfirmNewPasswordSerializer(serializers.Serializer):
    """
    Serializer for confirming a new password.

    - Requires: new_password + confirm_password
    - Ensures both values match.
    """
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        """Ensure new_password and confirm_password match."""
        new_password = attrs['new_password']
        confirm_password = attrs['confirm_password']

        if new_password != confirm_password:
            raise serializers.ValidationError('Password and confirm password does not match.')
        
        return attrs
