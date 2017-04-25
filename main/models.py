from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class account(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	handle = models.CharField(max_length=20)
	biography = models.CharField(max_length=300, default="My bio here...")

	def __str__(self):
		return self.handle
	
class spitt(models.Model):
	content = models.CharField(max_length=150)
	owner = models.ForeignKey(account)
	time_pub = models.DateTimeField(default=datetime.datetime.now, blank=True)

	def __str__(self):
		return self.content[:20] + "..."

	def timeAgo(self):
		return self.time_pub.strftime("%Y-%m-%d %H:%M:%S")

class image(models.Model):
	identifier = models.CharField(max_length=200, default='default.png')
	date_uploaded = models.DateTimeField(default=datetime.datetime.now, blank=True)
	usr = models.ForeignKey(account)

	def __str__(self):
		return str(self.usr) + " img"

class accFollowing(models.Model):
	follower = models.ForeignKey(account, related_name="follower_set")
	followee = models.ForeignKey(account, related_name="followee_set")

	def __str__(self):
		return str(self.follower) + " => " + str(self.followee)