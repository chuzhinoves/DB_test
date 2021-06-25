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
        new_obj = PipelineObject.objects.create(name="12", object_type=self.pump_type)
        self.assertEqual(len(signal_obj), 4)
        self.assertSetEqual(set(signal_obj), set(self.pump_type.signals.all()))
        new_signal = Signals.objects.create(name = "new_signal")
        SignalInfo.objects.create(object_signal=new_obj, signal=new_signal)
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

    def test_create_objects(self):
        tank1 = PipelineObject.objects.create(name='1', object_type=self.tank_type)
        tube1 = PipelineObject.objects.create(name='1', object_type=self.tube_type)
        pump1 = PipelineObject.objects.create(name='1', object_type=self.pump_type)
        tube2 = PipelineObject.objects.create(name='2', object_type=self.tube_type)
        tank2 = PipelineObject.objects.create(name='2', object_type=self.tank_type)
        Topology.objects.create(source=tank1, target=tube1)
        Topology.objects.create(source=tube1, target=pump1)
        Topology.objects.create(source=pump1, target=tube2)
        Topology.objects.create(source=tube2, target=tank2)
        self.assertSetEqual(tank1.sources.all(), tube1.targets.all())
    