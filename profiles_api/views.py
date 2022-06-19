from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

"""The status object from the rest framework is a list of handy HTTP status codes that you can use when returning 
responses from your API"""

from profiles_api import serializers


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

