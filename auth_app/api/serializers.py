from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import random
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class RegisterSerializer(serializers.ModelSerializer):
    confirmed_password = serializers.CharField(write_only=True)
    username = serializers.CharField(read_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        confirmed_password = attrs.get('confirmed_password')

        if password != confirmed_password:
            raise serializers.ValidationError('Password and confirmation do not match.')

        return attrs
    
    def create(self, validated_data):
        confirmed_password = validated_data.pop('confirmed_password')
        password = validated_data['password']
        email = validated_data['email']
        username = self.generate_unique_username(email)

        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.is_active=False
        user.save()
        return user


    def generate_unique_username(self, email):
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
    email = serializers.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "username" in self.fields:
            self.fields.pop('username')
     
    
    def validate(self, attrs):
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
    email = serializers.EmailField

    def validate(self, attrs):

        email = attrs['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return attrs
        
        attrs['user']=user

        return attrs