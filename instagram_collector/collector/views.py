from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .forms import TagForm
from urllib.request import urlopen
import json


# Create your views here.
def results (request):
	response=request.session.get('json_data')
	
	return HttpResponse( response)

def form(request):
	if request.method == 'POST':
		form = TagForm(request.POST)
		
		if(form.is_valid()):
			startDate = form.cleaned_data['start_date']
			endDate = form.cleaned_data['end_date']

			#TODO Authentication
			response = urlopen('https://api.instagram.com/v1/tags/'+form.cleaned_data['tag_name']+'/media/recent?client_id=b865ec47b91346f3a2cbcfe04a6a80d9')
			content = response.readall()
			jdata = json.loads(content.decode(encoding='utf-8' , errors='ignore'))
			# go through data find min/max tag id
			# find min/max time stamp
			# guesstimate min/max tag id that correspond with date
			# while current max tag <max tag
			# call service and add to jsondata
			request.session['json_data'] =str(content)
			# Store in DB
			return HttpResponseRedirect('/results/')
	else:
		form = TagForm()
	return render(request, 'form.html', {'form':form})