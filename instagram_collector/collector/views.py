"""view methods for instagram collector"""
from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import TagForm
import datetime
from datetime import datetime

import time
from .instagram_request import instagramrequest
from .models import Pix



# Create your views here.
def results(request):
    """this will generate the view for the result"""
    tag_name = request.session.get('tag_name')
    start_date = datetime.fromtimestamp(int(request.session.get('start_date')))
    end_date = datetime.fromtimestamp(int(request.session.get('end_date')))
    response = Pix.objects.filter(tag=tag_name).filter(date__gte=start_date).filter(date__lte=end_date)
    return render(request, 'result.html', {'pix_list':list(response)})

def form(request):
    if request.method == 'POST':
        form_data = TagForm(request.POST)    
        if form_data.is_valid():
            result = ''
            start_date = datetime.combine(form_data.cleaned_data['start_date'], datetime.min.time())
            end_date = datetime.combine(form_data.cleaned_data['end_date'], datetime.min.time())
            tag_name = form_data.cleaned_data['tag_name']
            #saving to session
            request.session['tag_name'] = tag_name
            request.session['start_date'] = time.mktime(start_date.timetuple())
            request.session['end_date'] = time.mktime(end_date.timetuple())

            jdata = instagramrequest(tag_name)
            # go through data find min/max tag id ( min > max)
            max_tag = int(jdata['pagination']['next_max_tag_id'])
            min_tag = int(jdata['pagination']['min_tag_id'])
            # find min/max time stamp
            min_time = datetime.today()
            max_time = datetime.fromtimestamp(0)
            for post in jdata['data'][:]:
                created_time = datetime.fromtimestamp(int(post['caption']['created_time']))
                min_time = min(created_time, min_time)
                max_time = max(created_time, max_time)
            # guesstimate min/max tag id that correspond with date
            # difference between time / difference between tag, results in tag/time
            tag_diff = min_tag - max_tag
            max_time_seconds = (max_time-datetime(1970, 1, 1)).total_seconds()
            min_time_seconds = (min_time-datetime(1970, 1, 1)).total_seconds()

            time_diff = max_time_seconds - min_time_seconds if max_time_seconds - min_time_seconds > 0 else 1
            # calculate the difference of min tag based on start date and today using tag/time

            tag_rate = tag_diff//time_diff # tags/second
            target_start_tag = max_tag-(abs(max_time-start_date).total_seconds()*tag_rate)
            target_end_tag = max_tag-(abs(min_time-end_date).total_seconds()*tag_rate)
            
            # while current max tag <max tag
            while target_start_tag < target_end_tag:
                
                temp_data = instagramrequest(tag_name, target_start_tag)
                #loop through each post
                for post in temp_data['data']:
                    created_time = datetime.fromtimestamp(int(post['created_time']))
                    if tag_name in post['tags']:
                        pic = Pix.objects.create_pix(date=created_time, tag=tag_name, piclink=post['images']['standard_resolution']['url'])
                    else:
                        #look in comments
                        for comment in post['comments']['data']:
                            if tag_name in comment:
                                pic = Pix.objects.create_pix(date=created_time, tag=tag_name, piclink=post['images']['standard_resolution']['url'])
                                break
                    #save pic
                    if pic is not None:
                        pic.save()
                    else:
                        raise ValueError('cannot find tag')

                # call service and add to jsondata
                #save list in db
                
                result += str(temp_data)
                target_start_tag = int(temp_data['pagination']['next_max_tag_id'])
            request.session['json_data'] = result
            #__saveToDB(data)
            # Store in DB
            return HttpResponseRedirect('/results/')
    else:
        form_data = TagForm()
    return render(request, 'form.html', {'form':form_data})

    