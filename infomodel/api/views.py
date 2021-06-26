from rest_framework import viewsets
from rest_framework.decorators import action

from api.serializers import (PipelineObjectSerializer, TypeObjectSerializer,
                             SignalsSerializer, TypeSignalsSerializer,
                             SignalInfoSerializer, TopologySerializer)
from app.models import (PipelineObject, TypeObject,
                        Signals, TypeSignals, SignalInfo,
                        Topology)


class PipelineObjectViewSet(viewsets.ModelViewSet):
    serializer_class = PipelineObjectSerializer
    queryset = PipelineObject.objects.all()
    
    @action(detail=True, methods=['post'])
    def insert_in_objects(self, request, pk):
        data = request.data
        

    

class TypeObjectViewSet(viewsets.ModelViewSet):
    serializer_class = TypeObjectSerializer
    queryset = TypeObject.objects.all()


class SignalsViewSet(viewsets.ModelViewSet):
    serializer_class = SignalsSerializer
    queryset = Signals.objects.all()