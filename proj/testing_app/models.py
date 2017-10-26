import json

from django.db import models


class DataSet(models.Model):
    set_id = models.IntegerField()
    upload_date = models.DateTimeField()
    status = models.NullBooleanField(blank=True)


class SetValues(models.Model):
    data_set = models.ForeignKey(DataSet, on_delete=models.CASCADE)
    value_a = models.IntegerField()
    value_b = models.IntegerField()
    result = models.TextField(blank=True)

    def load_values(self):
        return json.dumps({
            "pk": self.pk,
            "set_id": self.data_set.set_id,
            "a": self.value_a,
            "b": self.value_b
        })


class SetValuesError(models.Model):
    data_set = models.ForeignKey(DataSet, on_delete=models.CASCADE)
    err_date = models.DateTimeField()
    err = models.TextField()
    err_info = models.TextField()
