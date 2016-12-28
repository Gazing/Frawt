from rest_framework import serializers

class RoomSerializer(serializers.Serializer):
    room_name = serializers.CharField()
