import json

from django.shortcuts import render
from django.utils import timezone
from django.db.models import Max

from testing_app.tasks import add
from testing_app.models import DataSet, SetValues, SetValuesResult


def save_input_data(form):
    max_set_id = DataSet.objects.all().aggregate(Max('set_id'))
    if max_set_id.get('set_id__max'):
        set_id = max_set_id.get('set_id__max') + 1
    else:
        set_id = 1
    input_data = json.loads(form.get('text'))
    now = timezone.now()
    data_set = DataSet(set_id=set_id, upload_date=now).save()
    for values_index in range(len(input_data)):
        data = json.dumps({
            "set_id": set_id,
            "index": values_index,
            "a": input_data[values_index].get("a"),
            "b": input_data[values_index].get("b")
        })
        set_values = SetValues()
        set_values.save_values(data)


def index(request):
    form = request.POST
    if form:
        save_input_data(form)
        # j = json.loads(form.get('text'))
        # for element in j:
            # add.delay({"a": 2, "b": 3})
    return render(request, 'testing_app/index.html')
