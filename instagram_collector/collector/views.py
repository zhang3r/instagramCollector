from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .forms import TagForm
from urllib.request import urlopen
import json
# Create your views here.
def results (request):
	response='result'
	
	return HttpResponse( response)

def form(request):
	if request.method == 'POST':
		form = TagForm(request.POST)
		if(form.is_valid()):
			#TODO firing to instagram here
			response = urlopen('https://api.instagram.com/v1/tags/'+form.cleaned_data['tag_name']+'/media/recent?client_id=b865ec47b91346f3a2cbcfe04a6a80d9')
			content = response.readall()
			jdata = json.loads(content.decode(encoding='utf-8' , errors='ignore'))
			
			print(str(content))
			return HttpResponseRedirect('/results/')
	else:
		form = TagForm()
	return render(request, 'form.html', {'form':form})