from django.test import TestCase

from app.models import (PipelineObject, TypeObject,
                        Signals, TypeSignals, SignalInfo,
                        Topology)

class SignalsTest(TestCase):
    def setUp(self):
        self.valve_type = TypeObject.objects.create(name="valve")
        self.pump_type = TypeObject.objects.create(name="pump")
        self.pi = Signals.objects.create(name = "press_in")
        self.po = Signals.objects.create(name = "press_out")
        self.cls = Signals.objects.create(name = "close")
        self.opn = Signals.objects.create(name = "open")
        self.str = Signals.objects.create(name = "start")
        self.stp = Signals.objects.create(name = "stop")
        self.valve_type.signals.add(self.pi)
        self.valve_type.signals.add(self.po)
        self.valve_type.signals.add(self.cls)
        self.valve_type.signals.add(self.opn)
        self.pump_type.signals.add(self.pi)
        self.pump_type.signals.add(self.po)
        self.pump_type.signals.add(self.str)
        self.pump_type.signals.add(self.stp)
        PipelineObject.objects.create(name="234",
                                      object_type=self.valve_type)
        
    def test_created(self):
        valve = PipelineObject.objects.all()
        self.assertEqual(valve[0].name, "234")
        self.assertEqual(valve[0].object_type.name, "valve")
    
    def test_related(self):
        valve = PipelineObject.objects.filter(
            object_type__name = "valve"
        )

        self.assertTrue(valve.exists())
        self.assertEqual(valve[0].name, "234")

    def test_related2(self):
        valve_type = TypeObject.objects.get(
            name = "valve"
        )
        valve = valve_type.pipeline.all()
        self.assertTrue(valve.exists())
        self.assertEqual(valve[0].name, "234")
    
    def test_m2m_relation1(self):
        v_signal = self.valve_type.signals.all()
        p_signal = self.pump_type.signals.all()
        self.assertEqual(len(v_signal), 4)
        self.assertEqual(len(p_signal), 4)
        
    def test_m2m_relation2(self):
        self.assertEqual(len(self.pi.type.all()), 2)

    def test_m2m_through(self):
        type_signal = self.valve_type.type_signal.all()
        self.assertEqual(len(type_signal), 4)
        
    def test_craete_obj(self):
        print ('pipelineobject test create_objects\n')
        new_obj = PipelineObject.objects.create(name="12", object_type=self.pump_type)
        for type_signal in self.pump_type.type_signal.all():
            SignalInfo.objects.create(pipeline_object=new_obj,
                                      signal=type_signal.signal)
        
        signals_info = new_obj.signal_values.all()
        self.assertEqual(len(signals_info), 4)
        self.assertSetEqual(set(signals_info), set(SignalInfo.objects.all()))
        signal_obj = Signals.objects.filter(pipeline__pk=new_obj.pk)
        self.assertEqual(len(signal_obj), 4)
        self.assertSetEqual(set(signal_obj), set(self.pump_type.signals.all()))
        new_signal = Signals.objects.create(name = "new_signal")
        SignalInfo.objects.create(pipeline_object=new_obj, signal=new_signal)
        signal_obj = Signals.objects.filter(pipeline__pk=new_obj.pk)
        self.assertEqual(len(signal_obj), 5)
        self.assertIn(new_signal, signal_obj)

class TopologyTest (TestCase):
    def setUp(self):
        self.valve_type = TypeObject.objects.create(name="valve")
        self.pump_type = TypeObject.objects.create(name="pump")
        self.tube_type = TypeObject.objects.create(name="tube")
        self.tee_type = TypeObject.objects.create(name="tee")
        self.tank_type = TypeObject.objects.create(name='tank')
        self.tank1 = PipelineObject.objects.create(name='1', object_type=self.tank_type)
        self.tube1 = PipelineObject.objects.create(name='1', object_type=self.tube_type)
        self.pump1 = PipelineObject.objects.create(name='1', object_type=self.pump_type)
        self.tube2 = PipelineObject.objects.create(name='2', object_type=self.tube_type)
        self.tank2 = PipelineObject.objects.create(name='2', object_type=self.tank_type)
        Topology.objects.create(source=self.tank1, target=self.tube1)
        Topology.objects.create(source=self.tube1, target=self.pump1)
        Topology.objects.create(source=self.pump1, target=self.tube2)
        Topology.objects.create(source=self.tube2, target=self.tank2)

    def test_create_objects(self):
        print ('topology test create_objects\n')
        self.assertSetEqual(self.tank1.sources.all(), self.tube1.targets.all())
