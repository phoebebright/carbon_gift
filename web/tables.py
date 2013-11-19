import django_tables2 as tables
from web.models import *

class FootprintTable(tables.Table):

    name = tables.Column(verbose_name="full name")


    class Meta:

        model = Footprint
        exclude = ("id","object","created_by","created","updated", "notes")
