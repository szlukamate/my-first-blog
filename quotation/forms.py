from django import forms

from .models import tblDoc_details

class quotationroweditForm(forms.ModelForm):

    class Meta:
        model = tblDoc_details
        fields = ('firstnum_tblDoc_details', 'secondnum_tblDoc_details',)