import os
import uuid
from PIL import Image
from PIL.Image import LANCZOS

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.conf import settings

from .models import account, spitt, image, accFollowing

def createNewAccount(form_data):
	newUser = User(username=form_data['username'], password=make_password(form_data['password']), email=form_data['username'])
	newUser.save()
	newAccount = account(user=newUser, handle=form_data['handle'])
	newAccount.save()
	newAccountImg = image(usr=newAccount)
	newAccountImg.save()

def addNewSpitt(account, content):
	newSpitt = spitt(owner=account, content=content, time_pub=timezone.now())
	newSpitt.save()
	return newSpitt

def updateAccountBio(account, bio):
	account.biography = bio
	account.save()

def updateAccountImage(account, uploadedFile):
	img_name = str(uuid.uuid4()) + str(uploadedFile.name[uploadedFile.name.rfind('.'):])
	img = Image.open(uploadedFile)
	img.resize((150,150), LANCZOS).save(os.path.join(settings.BASE_DIR, 'main', 'images', os.path.basename(img_name)))

	newImage = image(usr=account, identifier=os.path.basename(img_name), date_uploaded=timezone.now())
	newImage.save()
	return newImage

def toggleFollowAccount(follower, followee):
	matchingObjects = accFollowing.objects.filter(follower=follower, followee=followee)
	if matchingObjects.count() < 1:
		newFollowPair = accFollowing(follower=follower, followee=followee)
		newFollowPair.save()
	else:
		oldFollowPair = matchingObjects[0]
		oldFollowPair.delete()