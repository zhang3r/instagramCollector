"""model class"""
from django.db import models

#pylint: disable=R0903
class PixManager(models.Manager):
    """manager for pix object"""
    def create_pix(self, date, tag, piclink):
        """model creator"""
        pic = self.create(date=date, tag=tag, piclink=piclink)
        return pic
# Create your models here.
class Pix(models.Model):
    """picture model"""
    date = models.DateField(blank=False)
    tag = models.CharField(max_length=64)
    piclink = models.CharField(max_length=256)
    objects = PixManager()
