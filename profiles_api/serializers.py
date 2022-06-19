from rest_framework import serializers


class HelloSerializer(serializers.Serializer):
    # the second one is the class name

    """Serializes a name field for testing our APIView
    Serializers will make sure that the content pass that api is of the correct type
    that you want to require for that field"""
    name = serializers.CharField(max_length=10)
