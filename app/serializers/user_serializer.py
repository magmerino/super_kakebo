# user_serializer.py
from rest_framework import serializers
from app.models import User
from app.utils.hashing import hash_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'role', 'currency', 'language']

    def create(self, validated_data):
        try:
            password = validated_data.pop('password', None)
            hashed_password = hash_password(password=password)
            validated_data['password'] = hashed_password
            user = User.objects.create(**validated_data)
            return user
        except Exception as ex:
            raise ex
