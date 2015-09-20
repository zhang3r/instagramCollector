from django import forms

import datetime

class TagForm(forms.Form):
	forms.DateInput.input_type="date"
	tag_name = forms.CharField(required=True,label='enter tags separated by ",":', max_length=256)
	start_date = forms.DateField(required=True)
	end_date = forms.DateField(required=True)
