from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery import Task

import json

from testing_app.models import DataSet, SetValues, SetValuesError


class CallbackTask(Task):
    def __init__(self):
        self.set_id = None

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        SetValuesError(
            data_set = DataSet.objects.get(set_id=self.set_id),
            err = exc,
            err_info = einfo
        ).save()



@shared_task(bind=True, base=CallbackTask)
def f1(self, set_id, pk):
    self.set_id = set_id
    set_values = SetValues.objects.get(pk=pk)
    return set_values.load_values()


@shared_task(bind=True, base=CallbackTask)
def f2(self, data):
    data = json.loads(data)
    self.set_id = data.get('set_id')
    data['result'] = data["a"] / data["b"]
    return json.dumps(data)


@shared_task(bind=True, base=CallbackTask)
def f3(self, data):
    data = json.loads(data)
    self.set_id = data.get('set_id')
    pk = data.get('pk')
    set_values = SetValues.objects.get(pk=pk)
    set_values.result = data.get('result')
    set_values.save()
