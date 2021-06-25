from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app.models import (PipelineObject, TypeObject,
                        Signals, TypeSignals, SignalInfo,
                        Topology)

from api.serializers import (PipelineObjectSerializer, TypeObjectSerializer,
                             SignalsSerializer, TypeSignalsSerializer,
                             SignalInfoSerializer, TopologySerializer)

# Create your tests here.
class ApiTest (APITestCase):
    def setUp(self):
        self.pump_type = TypeObject.objects.create(name="pump")
        
    def test_create_pipelineobject(self):
        url = reverse('api:pipeline-list')
        data = {'name' : '123', 'object_type' : str(self.pump_type.pk)}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PipelineObject.objects.count(), 1)
        self.assertEqual(PipelineObject.objects.get().name, '123')
    
    def test_craate_pipeline_serializer(self):
        data = {'name' : '123', 'object_type' : str(self.pump_type.pk)}
        serializer = PipelineObjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        self.assertEqual(PipelineObject.objects.count(), 1)
        self.assertEqual(PipelineObject.objects.get().name, '123')

        