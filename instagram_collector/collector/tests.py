from django.test import TestCase
from django.test import Client
from .models import Pix
import datetime

# Create your tests here.
#MODEL TEST
class PixTestCase(TestCase):
	def setUp(self):
		Pix.objects.create(date=datetime.datetime.today(),tag='cats', piclink='http://www.google.com')

	def test_pix_set_up(self):
		pic = Pix.objects.get(tag='cats')
		self.assertEqual(pic.piclink,'http://www.google.com')

	def test_response_happy_path(self):
		c=Client()
		response = c.post('/getForm/',{'tag_name':'cats', 'start_date':'2015-09-24','end_date':'2015-09-25'})
		# we redirect when post is valid
		self.assertEqual(response.status_code,302)
	

### THESE TEST SHOULD FAIL so returns a 200 not redirecting!!!
	def test_response_startdate_gt_enddate(self):
		c=Client()
		response = c.post('/getForm/',{'tag_name':'cats', 'start_date':'2015-09-26','end_date':'2015-09-25'})
		self.assertEqual(response.status_code,200)

	def test_response_enddate_gt_today(self):
		c=Client()
		response = c.post('/getForm/',{'tag_name':'cats', 'start_date':'2015-09-26','end_date':'3015-09-25'})
		self.assertEqual(response.status_code,200)

	def test_response_notag(self):
		c=Client()
		response = c.post('/getForm/',{'start_date':'2015-09-26','end_date':'3015-09-25'})
		self.assertEqual(response.status_code,200)
