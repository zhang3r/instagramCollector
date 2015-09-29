# Instagram Collector

This applications goes hits instagram api and pulls posts that has the associated hashtag

##usage
Assuming postgres and django has been installed

1. navigate to data folder
2. start up postgres "postgres -D . "
3. start up django "python manage.py runserver"
4. go to localhost:8000
5. fill out the form
6. system should display data in a list

### Logic
The instagram endpoint takes in a tag and a max_tag_id in order to paginate.
However the tag ids are not associated with dates
Therefore the program guestimates start and end tag ids based on start and end dates.
Since this is guess work the posts are not 100% guarenteed to be between the dates.

### output
~~right now the program just dumps all of instagram json data into postgres.~~

~~the results page just print the json more work is needed to extract the image itself out of the data and create a template for the output.~~

example output:

![example output](http://puu.sh/krYbB/36772d0b62.jpg "output")



#### TODO
~~1. improve pagination - only get the correct dates~~

~~2. template results - provide a readable output~~

~~3. store images and dates instead of json dump~~

4. TESTS!!!!! Stop being lazy >:(
