from rest_framework import serializers
from django.contrib.auth.models import User
import os
from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    # image = serializers.SerializerMethodField()
    bio = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio']
        # fields = ['id', 'username', 'email','image', 'bio']
    
    # def get_image(self, user):
    #     main_url = os.getenv("MAIN_URL") #include inside .env
    #     return main_url + user.profile.avatar.url
    
    def get_bio(self, user):
        return user.profile.bio 
    

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'role', 'bio']