from rest_framework import serializers

class RoomSerializer(serializers.Serializer):
    room_name = serializers.CharField()

class ScheduleSerializer(serializers.Serializer):
    start = serializers.TimeField()
    end = serializers.TimeField()
    date = serializers.CharField()

class MessageSerializer(serializers.Serializer):
    error_code = serializers.CharField()
    message = serializers.CharField()

class ApiMessage():
    def __init__(self, msg, err):
        self.message = msg
        self.error_code = err

class TimeSerializer(serializers.Serializer):
    time = serializers.TimeField()
    day = serializers.CharField()