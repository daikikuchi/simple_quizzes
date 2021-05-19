from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category objects"""
    name = serializers.ChoiceField(choices=Category.CATEGORY_CHOICES)

    class Meta:
        model = Category
        fields = ('id', 'name')
        read_only_fields = ('id',)
