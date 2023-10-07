from rest_framework import serializers
from django.contrib.auth.models import User 
from .models import Writers, Task, Project 
from datetime import datetime
from knox.models import AuthToken

class UserWithTokenSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'token']

    def get_token(self,obj):
        try:
            token = AuthToken.objects.get(user=obj)
            return token.digest 
        except AuthToken.DoesNotExist:
            return None

        

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

class TaskSerializer(serializers.ModelSerializer):

    deadline = MMDDYYYYDateField()
    class Meta:
        model = Task
        fields = ['id', 'status', 'writer', 'client', 'book_balance', 'deadline']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


