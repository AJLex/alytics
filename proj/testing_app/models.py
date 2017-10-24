import json

from django.db import models
from django_celery_results.models import TaskResult


class DataSet(models.Model):
    set_id = models.IntegerField(primary_key=True)
    upload_date = models.DateTimeField()

class SetValues(models.Model):
    data_set = models.ForeignKey(DataSet, on_delete=models.CASCADE)
    values_id = models.IntegerField()
    value_a = models.IntegerField()
    value_b = models.IntegerField()

    def save_values(self, data):
        set_values_info = json.loads(data)
        self.data_set = DataSet.objects.get(set_id=set_values_info.get('set_id'))
        self.values_id = set_values_info.get('index') + 1
        self.value_a = set_values_info.get("a")
        self.value_b = set_values_info.get("b")
        self.save()

    def load_values(self):
        return json.dimps({
            "set_id": self.data_set.set_id,
            "values_id": self.values_id,
            "a": self.value_a,
            "b": self.value_b
        })


class SetValuesResult(models.Model):
    check_id = models.IntegerField()
    check_date = models.DateTimeField()
    data_set = models.ForeignKey(DataSet, on_delete=models.CASCADE)
    values_id = models.OneToOneField(SetValues, on_delete=models.CASCADE)
    task = models.OneToOneField(TaskResult, on_delete=models.CASCADE)
    status = models.BooleanField()

    def save_results(self, resuts):
        test_results = json.loads(results)
        self.check_id = test_results.get('check_id')
        self.check_date = test_results.get('check_date')
        self.data_set = DataSet.objects.get(set_id=test_results('set_id'))
        self.values_id = test_results.get('values_id')
        self.task = TaskResult.objects.get(id = test_results.get('id_task'))

    def load_results(self):
        return json.dumps({
            "check_id": self.check_id,
            "check_date": self.check_date,
            "set_id":self.data_set.set_id,
            "values_id": self.values_id,
            "id_task": self.task.id
        })
