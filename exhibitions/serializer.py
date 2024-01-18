from rest_framework import serializers

from .models import *


class ThematicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thematic
        fields = "__all__"


class ExhibitionSerializer(serializers.ModelSerializer):
    reactor = ThematicSerializer(read_only=True, many=True)

    class Meta:
        model = Exhibition
        fields = "__all__"

