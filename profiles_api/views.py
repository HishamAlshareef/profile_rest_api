from rest_framework.views import APIView  # We created Hello APIView class
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets  # We created Hello ViewSet class
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters  # Need to be clarify
from rest_framework.authtoken.views import ObtainAuthToken
# That comes with the Django restframework that we can use to generate an authtoken

from rest_framework.settings import api_settings

"""The status object from the rest framework is a list of handy HTTP status codes that you can use when returning 
responses from your API"""
#from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated  # Django rest framework has another handy
# permission that comes with it by default just called is authenticated

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions


# we're going to use this to tell our API view what data to expect when making post put and patch requests to our API

class HelloApiView(APIView):
    """Test API View"""
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put. delete)'
            'Is similar to a traditional Django View',
            'Gives you the most control over you application logic',
            'Is mapped manually to URLs'
        ]

        return Response({'message': 'Hello', 'an_apiview': an_apiview})  # Dictionary to Define Keys and values

    def post(self, request):
        """Create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # This retrieves the name field that we defined and
            # you can retrieve any field that you define in serializer.py
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    # HTTP put you typically do it to a specific URL primary key we have this PK
    # but we default it to None in case we don't want to support the PK in this particular API view

    def put(self, request, pk=None):
        """Handle updating an object"""
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """Handle a partial update of an object"""
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):  # The delete request is used for deleting objects in the database
        """Delete an object"""
        return Response({'method': 'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Return a hello message"""

        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code',
        ]

        return Response(({'message': 'Hello!', 'a_viewset': a_viewset}))

    def create(self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""
        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handle updating an object"""
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Handle removing an object"""
        return Response({'http_method': 'DELETE'})


# The update partial update and destroy to manage specific model objects in the database

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)  # Add a comma after TokenAuthentication
    # so that this gets created as a tuple instead of just a single item
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class UserLoginApiView(ObtainAuthToken):
    """Handle crating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


# Create a viewset for our profile feed items
class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)  # use the token authentication to authenticate requests
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()  # manage all of our profile feed item objects from our model in our viewset
    # serializer_class and validated and then the serializer.save function is called by default
    permission_classes = (
        permissions.UpdateOwnStatus,
       # IsAuthenticatedOrReadOnly
        IsAuthenticated
    )

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        # create function is a handy feature of the Django rest framework that allows you to
        # override the behavior or customize the behavior for creating objects through a Model Viewset
        serializer.save(user_profile=self.request.user)
        # The serializer is a model serializer so it has a save function assigned to it
        # and that save function is used to save the contents of the serializer to an object in the database

        # if the user has authenticated then the request will have a user associated to the authenticated user
