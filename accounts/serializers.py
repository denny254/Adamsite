from rest_framework import serializers
from django.contrib.auth.models import User 
from .models import Writers 
from datetime import datetime

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = { 'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], 
            validated_data['email'], 
            validated_data['password']
        )
        return user
    
class MMDDYYYYDateField(serializers.Field):
    def to_internal_value(self, data):
        try:
            return datetime.strptime(data, '%m/%d/%Y').date()
        except ValueError:
            raise serializers.ValidationError('Invalid date format. Use mm/dd/yyyy.')

    def to_representation(self, value):
        return value.strftime('%m/%d/%Y')

class WriterSerializer(serializers.ModelSerializer):

    date = MMDDYYYYDateField()
    class Meta:
        model = Writers
        fields = ['id', 'name', 'specialization', 'date', 'email', 'phone_number']
