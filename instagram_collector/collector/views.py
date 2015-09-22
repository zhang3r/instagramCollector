from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .forms import TagForm
from urllib.request import urlopen
import datetime
import json
import pymongo
from pymongo import MongoClient
import time

def __saveToDB(jsondata):
		client = MongoClient('localhost',27017)
		db = client['my_db']
		collection = db['pixlee']
		jsonID = db['pixlee'].insert_one(jsondata).inserted_id
		client.close()
# Create your views here.
def results (request):
	response=request.session.get('json_data')
	
	return HttpResponse( response)

def form(request):
	if request.method == 'POST':
		form = TagForm(request.POST)
		
		if(form.is_valid()):
			startDate = datetime.datetime.combine(form.cleaned_data['start_date'], datetime.datetime.min.time())
			endDate = datetime.datetime.combine(form.cleaned_data['end_date'], datetime.datetime.min.time())
			result=''
			data={}
			#TODO Authentication
			response = urlopen('https://api.instagram.com/v1/tags/'+form.cleaned_data['tag_name']+'/media/recent?client_id=b865ec47b91346f3a2cbcfe04a6a80d9')
			content = response.readall()
			jdata = json.loads(content.decode(encoding='utf-8' , errors='ignore'))
			# go through data find min/max tag id ( min > max)
			max_tag = int(jdata['pagination']['next_max_tag_id'])
			min_tag = int(jdata['pagination']['min_tag_id'])
			# find min/max time stamp
			minTime=datetime.datetime.today()
			maxTime=datetime.datetime.fromtimestamp(0)
			for post in jdata['data'][:]:
				minTime= min(datetime.datetime.fromtimestamp(int(post['caption']['created_time'])//1000.0), minTime)
				maxTime= max(datetime.datetime.fromtimestamp(int(post['caption']['created_time'])//1000.0), maxTime)
			# guesstimate min/max tag id that correspond with date
			# difference between time / difference between tag, results in tag/time
			tag_diff = min_tag - max_tag
			maxTimeSeconds = (maxTime-datetime.datetime(1970,1,1)).total_seconds()
			minTimeSeconds = (minTime-datetime.datetime(1970,1,1)).total_seconds()

			time_diff =  maxTimeSeconds- minTimeSeconds if maxTimeSeconds- minTimeSeconds > 0 else 1
			# calculate the difference of min tag based on start date and today using tag/time

			tag_rate = tag_diff//time_diff
			target_start_tag = (maxTime-startDate).total_seconds()*tag_rate
			target_end_tag = (minTime-endDate).total_seconds()*tag_rate
			# while current max tag <max tag
			while( target_start_tag<target_end_tag):
				tempResponse = urlopen('https://api.instagram.com/v1/tags/'+form.cleaned_data['tag_name']+'/media/recent?client_id=b865ec47b91346f3a2cbcfe04a6a80d9&max_tag_id='+target_start_tag)
				tempContent = tempResponse.readall()
				tempData = json.loads(content.decode(encoding='utf-8' , errors='ignore'))
				# call service and add to jsondata
				data+=tempContent
				result+=str(tempContent)
				target_start_tag=int(tempContent['pagination']['next_max_tag_id'])
			request.session['json_data'] =result
			__saveToDB(data)
			# Store in DB
			return HttpResponseRedirect('/results/')
	else:
		form = TagForm()
	return render(request, 'form.html', {'form':form})

	