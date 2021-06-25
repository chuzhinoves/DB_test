from django.db import models


class PipelineObject (models.Model):
    name = models.CharField(max_length=200)
    object_type = models.ForeignKey("TypeObject",
                                    related_name="pipeline",
                                    on_delete=models.CASCADE)
    signals = models.ManyToManyField("Signals", related_name="pipeline",
                                          through="SignalInfo",
                                          through_fields=('pipeline_object', 'signal'))

class Topology (models.Model):
    source = models.ForeignKey('PipelineObject', related_name='sources', on_delete=models.CASCADE)
    target = models.ForeignKey('PipelineObject', related_name='targets', on_delete=models.CASCADE)


class TypeObject(models.Model):
    name = models.CharField(max_length=200)

    signals = models.ManyToManyField("Signals",
                                     related_name='type',
                                     through='TypeSignals',
                                     through_fields=('object_type', 'signal'))


class Signals (models.Model):
    name = models.CharField(max_length=200)


class SignalInfo (models.Model):
    pipeline_object = models.ForeignKey("PipelineObject", related_name="signal_values",
                                      on_delete=models.CASCADE, null=True)
    signal = models.ForeignKey("Signals", related_name="signal_values",
                                      on_delete=models.CASCADE, null=True)
    ip = models.IntegerField(null=True)


class TypeSignals(models.Model):
    signal = models.ForeignKey("Signals", on_delete=models.CASCADE,
                               related_name='type_signal')
    object_type = models.ForeignKey("TypeObject", on_delete=models.CASCADE,
                                    related_name='type_signal')
