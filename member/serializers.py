from django.contrib.auth.models import User, Group
from .models import PersonalInfo
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username','email', 'is_staff', 'password']
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        
        return user
        
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
        
class PersonalInfoSerializer(serializers.HyperlinkedModelSerializer):
    
    def create(self, validated_data):
        username = self.context['author']
        if username:
            # print("---------user---------", username)
            post = PersonalInfo.create(self, validated_data, username)
        
        return post
    class Meta:
        model = PersonalInfo
        fields = [
            'first_name', 
            'last_name', 
            'avatar', 
            'title', 
            'description', 
            'linkedin_url', 
            'github_url', 
            'personal_url'
        ]