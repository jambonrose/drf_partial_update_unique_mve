"""ModelSerializers demonstrating problem for MVE"""
from rest_framework.serializers import (
    CharField,
    DateField,
    IntegerField,
    Serializer,
    SlugField,
)
from rest_framework.validators import UniqueForMonthValidator

from .models import UniquePost


class PostSerializer(Serializer):
    """Working serializer"""

    id = IntegerField(label="ID", read_only=True)
    title = CharField(max_length=63)
    slug = SlugField(max_length=63)
    pub_date = DateField(required=False)


class UniquePostSerializer(Serializer):
    """Serializer that will fail to update partially"""

    id = IntegerField(label="ID", read_only=True)
    title = CharField(max_length=63)
    slug = SlugField(max_length=63)
    pub_date = DateField(required=False)

    class Meta:
        validators = [
            UniqueForMonthValidator(
                queryset=UniquePost.objects.all(), field="slug", date_field="pub_date"
            )
        ]
