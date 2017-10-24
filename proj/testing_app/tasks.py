from __future__ import absolute_import, unicode_literals
from celery import shared_task
import json


@shared_task
def add(data_dict):
    return data_dict.get("a") + data_dict.get("b")
