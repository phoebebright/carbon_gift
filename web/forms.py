from django.forms import ModelForm
from django import forms

from web.models import *

class FootprintForm(ModelForm):

    class Meta:
        model = Footprint
        widgets = {'created_by': forms.HiddenInput,
                   "object": forms.HiddenInput,
                   "verified": forms.HiddenInput,
                   "source": forms.TextInput(attrs={'size':'60'}),
                   "size": forms.TextInput(attrs={'size':'6'}),
                   }



