"""instagram request module"""
from urllib.request import urlopen
import json

def instagramrequest(tag_name, max_tag_id=0):
    """ this returns the json data of the request"""
    request_string = '?client_id=b865ec47b91346f3a2cbcfe04a6a80d9'
    if max_tag_id:
        request_string += '&max_tag_id='+str(max_tag_id)
    response = urlopen('https://api.instagram.com/v1/tags/'+tag_name+'/media/recent'+request_string)
    content = response.readall()
    return json.loads(content.decode(encoding='utf-8', errors='ignore'))


