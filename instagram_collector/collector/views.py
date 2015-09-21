from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .forms import TagForm
from urllib.request import urlopen
import datetime
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
			result=''
			#TODO Authentication
			response = urlopen('https://api.instagram.com/v1/tags/'+form.cleaned_data['tag_name']+'/media/recent?client_id=b865ec47b91346f3a2cbcfe04a6a80d9')
			content = response.readall()
			jdata = json.loads(content.decode(encoding='utf-8' , errors='ignore'))
			# go through data find min/max tag id ( min > max)
			max_tag = jdata['pagination']['next_max_tag_id']
			min_tag = jdata['pagination']['min_tag_id']
			# find min/max time stamp
			minTime=datetime.date.today()
			maxTime=0
			for post in jdata['data'][:]:
				minTime= min(post['caption']['created_time'], minTime)
				maxTime= max(post['caption'], maxTime)
			# guesstimate min/max tag id that correspond with date
			# difference between time / difference between tag, results in tag/time
			tag_diff = min_tag - max_tag
			time_diff = maxTime - minTime
			# calculate the difference of min tag based on start date and today using tag/time
			tag_rate = tag_diff//time_diff.total_seconds()
			target_start_tag = (maxTime-startDate).total_seconds()*tag_rate
			target_end_tag = (minTime-endDate).total_seconds()*tag_rate
			# while current max tag <max tag
			while( target_start<target_end):
				tempResponse = urlopen('https://api.instagram.com/v1/tags/'+form.cleaned_data['tag_name']+'/media/recent?client_id=b865ec47b91346f3a2cbcfe04a6a80d9&max_tag_id='+target_start_tag)
				tempContent = tempResponse.readall()
				tempData = json.loads(content.decode(encoding='utf-8' , errors='ignore'))
				# call service and add to jsondata
				result+=str(tempContent)
				target_start=tempContent['pagination']['next_max_tag_id']
			request.session['json_data'] =result
			# Store in DB
			return HttpResponseRedirect('/results/')
	else:
		form = TagForm()
	return render(request, 'form.html', {'form':form})