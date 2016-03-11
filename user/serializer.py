from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Interviewee


class InterviewRegistrationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=20, style={'placeholder': 'Bertil Andersson'})
    matricNumber = serializers.CharField(max_length=9, style={'placeholder': 'U1234567A'}, label="Matric Number")
    major = serializers.CharField(style={'placeholder': 'EEE'})
    year = serializers.IntegerField(style={'placeholder': '3'})
    phone = serializers.IntegerField(style={'placeholder': '98765432'})

    class Meta:
        model = Interviewee
        field = ['name', 'matricNumber', 'year', 'major', 'phone', ]
        exclude = ('user',)


class IntervieweeRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    password = serializers.CharField(source='user.password', write_only=True)

    class Meta:
        model = Interviewee
        fields = ('id', 'username', 'password', 'name', 'matricNumber', 'year', 'major', 'phone')

    def update(self, instance, validated_data):
        print(instance)
        print(validated_data)
        if instance is not None:
            q = validated_data.pop('user', None)
            q.pop('username', None)
        interviewee = super(IntervieweeRegistrationSerializer, self).update(instance, validated_data)
        if 'password' in q:
            interviewee.user.set_password(q['password'])
            interviewee.user.save()
        return interviewee

    def create(self, validated_data):
        info = validated_data.pop('user')
        print(info)
        user = User.objects.create_user(username=info.get('username'), password=info.get('password'))
        validated_data['user'] = user
        return super(IntervieweeRegistrationSerializer, self).create(validated_data)

