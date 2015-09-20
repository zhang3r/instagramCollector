from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import TagForm

# Create your views here.
def results (request, tagRequest_id):
	response="tag response"
	return HTTPResponse( response)

def form(request):
	if request.method == 'POST':
		form = TagForm(request.POST)
		if(form.is_valid()):
			return HttpResponseRedirect('/results/')
	else:
		form = TagForm()
	return render(request, 'form.html', {'form':form})