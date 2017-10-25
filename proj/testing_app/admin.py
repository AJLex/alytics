from django.contrib import admin
from testing_app.models import DataSet, SetValues, SetValuesError


admin.site.register(DataSet)
admin.site.register(SetValues)
admin.site.register(SetValuesError)
