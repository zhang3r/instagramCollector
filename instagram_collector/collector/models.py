from django.db import models

class PixManager(models.Manager):
	def create_pix(self, date, tag, piclink):
		pic = self.create(date=date,tag=tag, piclink=piclink)
		return pic
# Create your models here.
class Pix(models.Model):
	date = models.DateField(blank=False)
	tag = models.CharField(max_length=64)
	piclink = models.CharField(max_length=256)
	objects=PixManager()

