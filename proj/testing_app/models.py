from django.db import models
from django_celery_results.models import TaskResult

class DataSet(models.Model):
    set_number = models.IntegerField()
    upload_date = models.DateTimeField('upload date')

    def __str__(self):
        return self.set_number, self.upload_date

class SetValues(models.Model):
    value_a = models.IntegerField('value a')
    value_b = models.IntegerField('value b')
    set_number = models.ForeignKey(DataSet, on_delete=models.CASCADE)
    task_id = models.OneToOneField(TaskResult,on_delete=models.CASCADE)

    def __srt__(self):
        return self.set_number, self.value_a, self.value_b, self.task_id
