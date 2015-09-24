# instagramCollector

This applications goes hits instagram api and pulls posts that has the associated hashtag

##usage

1. navigate to data folder
2. start up postgres "postgres -D . "
3. start up django "python manage.py runserver"
4. go to localhost:8000

### Logic
The instagram endpoint takes in a tag and a max_tag_id in order to paginate.
However the tag ids are not associated with dates
Therefore the program guestimates start and end tag ids based on start and end dates.
Since this is guess work the posts are not 100% guarenteed to be between the dates.

### output
right now the program just dumps all of instagram json data into postgres.

the results page just print the json more work is needed to extract the image itself out of the data and create a template for the output.
