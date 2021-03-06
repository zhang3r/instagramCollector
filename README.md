# Instagram Collector

This applications goes hits instagram api and pulls posts that has the associated hashtag made with django and python 3.

now mostly pylinter friendly

##usage
Assuming postgres and django has been installed

1. navigate to data folder
2. start up postgres "postgres -D . "
3. start up django "python manage.py runserver" ~~or "django-admin runserver"~~
4. open browser to http://localhost:8000
5. fill out the form
6. page should display results in a list

### Logic
The instagram endpoint takes in a tag and a max_tag_id in order to paginate.
However the tag ids are not associated with dates
Therefore the program guestimates start and end tag ids based on start and end dates.
Since this is guess work the posts are not 100% guarenteed to be between the dates.

This is done due to the limits raised by instagram noted [here: limits](https://instagram.com/developer/limits/)

at 5000 requests/hour at 20 items per request, at max instagram allows you to query 100,000 posts/hour. Therefore in an attempt to increase result requests and decrease the number of requests needed to find valid tag ids, an hueristic is applied in finding tag ids to start gather posts. However this comes at a cost of accuracy and completeness.

### output

example output:

![example output](http://puu.sh/krYbB/36772d0b62.jpg "output")


#### TESTING
To run tests, navigate to base directory and run "python manage.py test --settings instagram_collector.unittestsettings"

