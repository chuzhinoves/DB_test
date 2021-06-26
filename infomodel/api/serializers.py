from django.db.models import fields
from rest_framework import serializers

from app.models import (PipelineObject, TypeObject,
                        Signals, TypeSignals, SignalInfo,
                        Topology)


class TypeObjectSerializer (serializers.ModelSerializer):
    class Meta:
        model = TypeObject
        fields = '__all__'


class PipelineObjectSerializer (serializers.ModelSerializer):
    object_type = PipelineObjectSerializer(read_only=True)
    class Meta:
        model = PipelineObject
        fields = '__all__'

 
class SignalsSerializer (serializers.ModelSerializer):
    class Meta:
        model = Signals
        fields = '__all__'


class TypeSignalsSerializer (serializers.ModelSerializer):
    object_type = PipelineObjectSerializer(read_only=True)
    signal = SignalsSerializer(read_only=True)
    class Meta:
        model = TypeSignals
        fields = '__all__'


class SignalInfoSerializer (serializers.ModelSerializer):
    class Meta:
        model = SignalInfo
        fields = '__all__'


class TopologySerializer (serializers.ModelSerializer):
    class Meta:
        model = Topology
        fields = '__all__'