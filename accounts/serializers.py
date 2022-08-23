import  math
from kivy import require
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from accounts.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import *
from django.contrib.auth.models import update_last_login
from django.contrib.auth import password_validation


class UserSerializer(serializers.ModelSerializer):
    # user_type = ChoiceField(choices=user_types, source='get_user_type')
    user_type_value = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ['password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'groups', 'date_joined']
        # fields = '__all__'

    def get_user_type_value(self, obj):
        return obj.get_user_type_display()


class ResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10000

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'current_page': int(self.request.query_params.get('page', 1)),
            'total': self.page.paginator.count,
            # 'per_page': self.page_size,
            'total_pages':  math.floor(self.page.paginator.count / self.page_size),
            'results': data,
        })

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        email = data.get("email")
        print(email, 'email')
        password = data.get("password")
        print(password, 'pass')
        if User.objects.filter(email=email).exists():
            user = authenticate(username=email, password=password)
            print(user, 'users')
        else:
            raise serializers.ValidationError(
                'Email doesnot exists.'
            )
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        try:
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return {
            'email': user.email,
        }

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


# class TimerSerializers(serializers.ModelSerializer):
#     class Meta:
#         model=Timer
#         fields=['start','stop']

class TimeSerializer(serializers.Serializer):
    start = serializers.CharField(max_length=255)
    stop = serializers.CharField(max_length=128, required=False)        