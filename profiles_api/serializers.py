from rest_framework import serializers

from profiles_api import models


class HelloSerializer(serializers.Serializer):
    # the second one is the class name

    """Serializes a name field for testing our APIView
    Serializers will make sure that the content pass that api is of the correct type
    that you want to require for that field"""
    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = (
            'id', 'email', 'name', 'password')  # either make accessible in our API or you want to use to create new
        # models with our serializer
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        """You want to make sure it's within the serializer class not inside the meta class"""
        user = models.UserProfile.objects.create_user(
            # to create and return a new user from our user profiles model manager
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        return user


class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serializes profile feed items"""

    class Meta:
        model = models.ProfileFeedItem
        # This sets our serializer or our model serializer to our profile feed item model that we created in models.py

        fields = ('id', 'user_profile', 'status_text', 'created_on')
        # The 'id' is set up by Django by default it's automatically set to read only
        extra_kwargs={'user_profile':{'read_only':True}}


    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)
