from __future__ import absolute_import, unicode_literals
import json

from celery import shared_task
from celery import Task
from django.utils import timezone

from testing_app.models import DataSet, SetValues, SetValuesError


# Сlass needs to be able to write an exception
class CallbackTask(Task):
    def __init__(self):
        self.set_id = None
        self.pk = None

    #  Function writes the arisen exceptions  into the database,
    #  updates values calculation result status and updates data set status
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        data_set = DataSet.objects.get(set_id=self.set_id)
        SetValuesError(
            data_set=data_set,
            err=exc,
            err_info=einfo,
            err_date=timezone.now()
        ).save()
        set_values = SetValues.objects.filter(data_set=data_set).get(pk=self.pk)
        set_values.result = exc
        set_values.save()
        if data_set.status is not False:
            data_set.status = False
            data_set.save()


@shared_task(bind=True, base=CallbackTask)
def load_set_values(self, set_id, pk):
    self.set_id = set_id
    self.pk = pk
    set_values = SetValues.objects.get(pk=pk)
    return set_values.load_values()


@shared_task(bind=True, base=CallbackTask)
def test_func(self, data):
    data = json.loads(data)
    self.set_id = data.get('set_id')
    self.pk = data.get('pk')
    data['result'] = data["a"] + data["b"]
    return json.dumps(data)


@shared_task(bind=True, base=CallbackTask)
def save_test_func_result(self, data):
    data = json.loads(data)
    self.set_id = data.get('set_id')
    pk = data.get('pk')
    self.pk = data.get('pk')
    set_values = SetValues.objects.get(pk=pk)
    set_values.result = data.get('result')
    set_values.save()
    data_set = DataSet.objects.get(set_id=self.set_id)
    if not data_set.status:
        data_set.status = True
        data_set.save()
