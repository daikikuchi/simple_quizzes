from rest_framework import serializers

from .models import Category, Question


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category objects"""
    name = serializers.ChoiceField(choices=Category.CATEGORY_CHOICES)

    class Meta:
        model = Category
        fields = ('id', 'name')
        read_only_fields = ('id', 'name')


class CategoryPKField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        queryset = Category.objects.filter(user=user)
        return queryset


class QuestionSerializer(serializers.ModelSerializer):
    category = CategoryPKField()

    class Meta:
        model = Question
        fields = ['id', 'content', 'answer', 'category', 'created_at']
        read_only_fields = ('id',)


class QuestionDetailSerializer(QuestionSerializer):
    category = CategorySerializer(read_only=True)
