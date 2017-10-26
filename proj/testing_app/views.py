import json

from celery import chain
from django.shortcuts import render
from django.db.models import Max
from django.utils import timezone

from testing_app.models import DataSet, SetValues, SetValuesError
from testing_app.tasks import load_set_values, test_func, save_test_func_result


#  Function saves input informations in data base
def save_input_data(form):
    # Getting id of last added set
    max_set_id = DataSet.objects.all().aggregate(Max('set_id'))
    if max_set_id.get('set_id__max'):
        set_id = max_set_id.get('set_id__max') + 1
    else:
        # If no set where added id of set is 1
        set_id = 1
    data_set = DataSet(set_id=set_id, upload_date=timezone.now()).save()
    try:
        #  If the input data is incorrect, raises an exception and writing aborted
        input_data = json.loads(form.get('text'))
        for values_index in range(len(input_data)):
            # If input data is OK, values write to data base
            SetValues(
                data_set = DataSet.objects.get(set_id=set_id),
                value_a = int(input_data[values_index]['a']),
                value_b = int(input_data[values_index]['b'])
            ).save()
    except :
        data_set = DataSet.objects.get(set_id=set_id).delete()


# Function starts calculation with using different queues
def starting_calculation(sets):
    for data_set in sets:
        set_id = data_set.set_id
        values = SetValues.objects.filter(data_set=data_set)
        for set_values in values:
            pk = set_values.pk
            # Starting tasks chain
            chain(
                load_set_values.signature(args=(set_id, pk),queue='fir'),
                test_func.signature(queue='sec'),
                save_test_func_result.signature(queue='thi')
            )()


# Function gets result executing calculation if any
def get_results(sets, context):
    if sets.filter(status=False):
        context = {"main_status": False}
    else:
        context = {"main_status": True}
    context['values'] = SetValues.objects.all().order_by('data_set')
    context['exceptions'] = SetValuesError.objects.all()
    return context


def index(request):
    form = request.POST
    sets = DataSet.objects.all()
    context = {}
    if form.get('save'):
        save_input_data(form)
    if form.get('calc') and sets:
        starting_calculation(sets)
    if sets:
        context = get_results(sets, context)
    return render(request, 'testing_app/index.html', context)
