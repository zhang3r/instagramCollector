# Instagram Collector

This applications goes hits instagram api and pulls posts that has the associated hashtag

##usage
Assuming postgres and django has been installed

1. navigate to data folder
2. start up postgres "postgres -D . "
3. start up django "python manage.py runserver" ~~or "django-admin runserver"~~
4. open browser to http://localhost:8000
5. fill out the form
6. system should display data in a list

### Logic
The instagram endpoint takes in a tag and a max_tag_id in order to paginate.
However the tag ids are not associated with dates
Therefore the program guestimates start and end tag ids based on start and end dates.
Since this is guess work the posts are not 100% guarenteed to be between the dates.

### output

example output:

![example output](http://puu.sh/krYbB/36772d0b62.jpg "output")


#### TESTING
To run tests, navigate to base directory and run "python manage.py test --settings instagram_collector.unittestsettings"

