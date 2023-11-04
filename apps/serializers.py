from rest_framework import serializers
from .models import (
    Writers, 
    Task,
    Project,
    RegisterUser,
    )
from datetime import datetime
from django.contrib.auth import authenticate


class userSerializer(serializers.ModelSerializer):
   

    class Meta:
        model = RegisterUser
        fields = ['id', 'email', 'first_name', 'last_name',
                  'username', 'phone_number', 'password']

class CreateUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RegisterUser 
        fields = '__all__'

        extra_kwargs = {
            'password':{'required': True}
            }



    def validate(self, attrs):
        email = attrs.get('email', '').strip().lower()
        if RegisterUser.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': ('Email is already in use')})
        
        return attrs
    
    def create(self, validated_data):
        user = RegisterUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
        )
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterUser
        fields = ['id', 'email', 'first_name', 'last_name',
                  'username', 'phone_number', 'password']
        
    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        if password:
            instance.set_password(password)
        instance = super().update(instance, validated_data)
        return instance  
   
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(write_only=True, trim_whitespace=False)


    def validate(self, attrs):
        email = attrs.get('email').lower()
        password = attrs.get('password', '')

        if not email or not password:
            raise serializers.ValidationError(
                'Please provide both email and password to login')
        

        if not  RegisterUser.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Email does not exist.')
        user = authenticate(request=self.context.get('request'),
                            email=email, password=password)
           
        if not user:
            raise serializers.ValidationError(
                'Wrong Credentials. Please try again')
        
        attrs['user'] = user 
        return attrs 
           




    
class YYYYMMDDDateField(serializers.Field):
    def to_internal_value(self, data):
        try:
            return datetime.strptime(data, '%Y/%m/%d').date()
        except ValueError:
            raise serializers.ValidationError('Invalid date format. Use yyyy/mm/dd.')

    def to_representation(self, value):
        return value.strftime('%Y/%m/%d')


class WriterSerializer(serializers.ModelSerializer):

    date = YYYYMMDDDateField()
    class Meta:
        model = Writers
        fields = ['id', 'name', 'specialization', 'date', 'email', 'phone_number']

class TaskSerializer(serializers.ModelSerializer):

    deadline = YYYYMMDDDateField()
    class Meta:
        model = Task
        fields = ['id', 'status', 'writer', 'client', 'book_balance', 'deadline']

class ProjectSerializer(serializers.ModelSerializer):

    deadline = YYYYMMDDDateField() 

    class Meta:
        model = Project
        fields = '__all__'


