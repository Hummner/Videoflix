from rest_framework import serializers
from django.contrib.auth.models import User
import random



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