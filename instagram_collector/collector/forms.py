from django import forms
from django.core.exceptions import ValidationError
import datetime

class TagForm(forms.Form):
	forms.DateInput.input_type="date"
	tag_name = forms.CharField(required=True,label='enter tags separated by ",":', max_length=256)
	start_date = forms.DateField(required=True)
	end_date = forms.DateField(required=True)
	def clean(self):
		if self.cleaned_data.get('start_date') > self.cleaned_data.get('end_date'):
			raise ValidationError("end date must be greater than start date")
		if self.cleaned_data.get('end_date')>datetime.date.today():
			raise ValidationError("end date cannot be in the future")
		return self.cleaned_data