#app
#from web.forms import TransactForm
from web.models import *
from web.forms import *

#django
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic.base import View
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from django_tables2 import SingleTableView
import django_tables2 as tables

#python
import json
import csv
from datetime import datetime,timedelta, date


class Home(TemplateView):


    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['required'] = Object.objects.filter(feet__lte=3)
        return context

class PointsView(TemplateView):


    template_name = "points.html"

    def get_context_data(self, **kwargs):
        context = super(PointsView, self).get_context_data(**kwargs)
        context['required'] = Points.objects.filter(user=self.request.user)
        return context

class HelpView(TemplateView):


    template_name = "help.html"




class FootCreate(CreateView):
    model = Footprint
    form_class = FootprintForm
    fields = ["source","size","notes", "created_by","object"]
    success_url = reverse_lazy('home')

    def get_initial(self):
        object = Object.objects.get(id=self.kwargs['obj_id'])
        return { 'object': object, 'created_by': self.request.user }

    # add gift object to context so can display on form
    def get_context_data(self, **kwargs):
        object = Object.objects.get(id=self.kwargs['obj_id'])
        kwargs['object'] = object

        return kwargs

    #def form_valid(self, form):
    #    form.instance.object
    #    form.instance.created_by = self.request.user
    #    return super(FootCreate, self).form_valid(form)



class FootUpdate(UpdateView):
    model = Footprint
    success_url = reverse_lazy('home')

class FootDelete(DeleteView):
    model = Footprint
    success_url = reverse_lazy('home')



class FootprintTable(tables.Table):
    class Meta:
        model = Footprint
        fields = ('object.name', 'size', 'created', 'verified')
        template_name = "web/footprint_list.html"



class FootList(SingleTableView):

    table_class = FootprintTable


    def get_queryset(self):
        # user can only view updates for their organisation

        return Footprint.objects.filter(created_by=self.request.user)

