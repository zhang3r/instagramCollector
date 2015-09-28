from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .forms import TagForm
from urllib.request import urlopen
import datetime
import json
import psycopg2
import time
from psycopg2.extras import Json
from .models import Pix, PixManager


#def __saveToDB(jsondata):
	#try:
		#conn = psycopg2.connect("host='localhost' dbname='mydb' user='Zhang3r' password='password'")
		#cur = conn.cursor()
	
		#cur.execute("insert into myData (data) values (%s)",[Json(jsondata)])
		#conn.close()
	#except:
	#	raise ValueError('error connecting to db.')
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
			tagName = form.cleaned_data['tag_name']
			result=''
			data={}
			pics =[]
			#TODO Authentication
			response = urlopen('https://api.instagram.com/v1/tags/'+tagName+'/media/recent?client_id=b865ec47b91346f3a2cbcfe04a6a80d9')
			content = response.readall()
			jdata = json.loads(content.decode(encoding='utf-8' , errors='ignore'))
			# go through data find min/max tag id ( min > max)
			max_tag = int(jdata['pagination']['next_max_tag_id'])
			min_tag = int(jdata['pagination']['min_tag_id'])
			# find min/max time stamp
			minTime=datetime.datetime.today()
			maxTime=datetime.datetime.fromtimestamp(0)
			for post in jdata['data'][:]:
				minTime= min(datetime.datetime.fromtimestamp(int(post['caption']['created_time'])), minTime)
				maxTime= max(datetime.datetime.fromtimestamp(int(post['caption']['created_time'])), maxTime)
			# guesstimate min/max tag id that correspond with date
			# difference between time / difference between tag, results in tag/time
			tag_diff = min_tag - max_tag
			maxTimeSeconds = (maxTime-datetime.datetime(1970,1,1)).total_seconds()
			minTimeSeconds = (minTime-datetime.datetime(1970,1,1)).total_seconds()

			time_diff =  maxTimeSeconds- minTimeSeconds if maxTimeSeconds- minTimeSeconds > 0 else 1
			# calculate the difference of min tag based on start date and today using tag/time

			tag_rate = tag_diff//time_diff # tags/second
			target_start_tag = max_tag-(abs(maxTime-startDate).total_seconds()*tag_rate)
			target_end_tag = max_tag-(abs(minTime-endDate).total_seconds()*tag_rate)
			
			# while current max tag <max tag
			while( target_start_tag<target_end_tag):
				tempResponse = urlopen('https://api.instagram.com/v1/tags/'+tagName+'/media/recent?client_id=b865ec47b91346f3a2cbcfe04a6a80d9&max_tag_id='+str(target_start_tag))
				tempContent = tempResponse.readall()
				tempData = json.loads(content.decode(encoding='utf-8' , errors='ignore'))
				#loop through each post
				for post in tempData['data']:
					if tagName in post['tags']:
						pic=Pix.objects.create_pix(date=datetime.datetime.fromtimestamp(int(post['created_time'])), tag= tagName, piclink=post['images']['standard_resolution']['url'])
					else:
						#look in comments
						for comment in post['comments']['data']:
							if tagName in text:
								pic=Pix.objects.create_pix(date=datetime.datetime.fromtimestamp(int(comment['created_time'])), tag= tagName, piclink=post['images']['standard_resolution']['url'])
								break
					#save pic
					pic.save()

				# call service and add to jsondata
				#save list in db
				data.update(tempData)
				result+=str(tempData)
				target_start_tag=int(tempData['pagination']['next_max_tag_id'])
			request.session['json_data'] =result
			#__saveToDB(data)
			# Store in DB
			return HttpResponseRedirect('/results/')
	else:
		form = TagForm()
	return render(request, 'form.html', {'form':form})

	