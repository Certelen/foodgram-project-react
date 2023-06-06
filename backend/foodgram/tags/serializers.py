from rest_framework import serializers

from .models import Tags


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Tags
