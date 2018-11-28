"""ModelSerializers demonstrating problem for MVE"""
from rest_framework.serializers import ModelSerializer

from .models import Post, UniquePost


class PostSerializer(ModelSerializer):
    """Working serializer"""

    class Meta:
        model = Post
        fields = "__all__"


class UniquePostSerializer(ModelSerializer):
    """Serializer that will fail to update partially"""

    class Meta:
        model = UniquePost
        fields = "__all__"
