import json

from django.shortcuts import render

from testing_app.tasks import add


def index(request):
    form = request.POST
    if form:
        # j = json.loads(form.get('text'))
        # for element in j:
            add.delay({"a": 2, "b": 3})
    return render(request, 'testing_app/index.html')
