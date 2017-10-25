import sys
import json

from celery import chain
from django.shortcuts import render
from django.db.models import Max

from testing_app.models import DataSet, SetValues, SetValuesError
from testing_app.tasks import f1, f2, f3

def save_input_data(form):
    max_set_id = DataSet.objects.all().aggregate(Max('set_id'))
    if max_set_id.get('set_id__max'):
        set_id = max_set_id.get('set_id__max') + 1
    else:
        set_id = 1
    data_set = DataSet(set_id=set_id).save()
    try:
        input_data = json.loads(form.get('text'))
        for values_index in range(len(input_data)):
            SetValues(
                data_set = DataSet.objects.get(set_id=set_id),
                value_a = int(input_data[values_index]['a']),
                value_b = int(input_data[values_index]['b'])
            ).save()
    except Exception as msg:
        data_set = DataSet.objects.get(set_id=set_id)
        data_set.status = False
        data_set.save()
        SetValuesError(
            data_set = data_set,
            err = sys.exc_info()[0],
            err_info = sys.exc_info()
        ).save()



def index(request):
    form = request.POST
    if form.get('save'):
        save_input_data(form)
    if form.get('calc'):
        sets = DataSet.objects.all()
        for data_set in sets:
            set_id = data_set.set_id
            values = SetValues.objects.filter(data_set=data_set)
            if values:
                for set_values in values:
                    pk = set_values.pk
                    print(pk)
                    chain(
                        f1.signature(args=(set_id, pk),queue='fir'),
                        f2.signature(queue='sec'),
                        f3.signature(queue='thi')
                    )()

    return render(request, 'testing_app/index.html')
