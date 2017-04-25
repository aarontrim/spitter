import os

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
import django.contrib.auth
from django.contrib.auth.models import User

# Create your views here.
from .models import account, spitt
from .forms import SignupForm, LoginForm, SpittForm, BioForm, ImgForm
from .functions import createNewAccount, addNewSpitt, updateAccountBio, updateAccountImage, toggleFollowAccount
from django.conf import settings

def index(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('feed', args=(request.user.account.handle,)))
	else:
		return HttpResponseRedirect(reverse('login'))

def login(request):
	if not request.user.is_authenticated:
		if request.method == "POST":
			form = LoginForm(request.POST)
			if form.is_valid():			
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				user = django.contrib.auth.authenticate(username=username, password=password)
				django.contrib.auth.login(request, user)

				return HttpResponseRedirect(reverse('feed', args=(user.account.handle,)))
		else:
			form = LoginForm()

		return render(request, 'main/login.html', {'form': form})
	else:
		return HttpResponseRedirect(reverse('feed', args=(request.user.account.handle,)))		

def logout(request):
	django.contrib.auth.logout(request)

	return HttpResponseRedirect(reverse('index'))

def signup(request):
	if not request.user.is_authenticated:
		if request.method == "POST":
			form = SignupForm(request.POST)
			if form.is_valid():
				createNewAccount(form.cleaned_data)
				return HttpResponseRedirect(reverse('index'))
			else:
				return render(request, 'main/signup.html', {'form': form})
		else:
			form = SignupForm()
			return render(request, 'main/signup.html', {'form': form})
	else:
		return HttpResponseRedirect(reverse('feed', args=(request.user.account.handle,)))		
		

def getimage(request, file_name):
	file_path = os.path.join(settings.BASE_DIR, 'main', 'images', os.path.basename(file_name))
	if os.path.exists(file_path):
		f = open(file_path, "rb+")
		return HttpResponse(f.read(), content_type="image/jpeg")
	else:
		raise Http404

def discover(request):
	users = User.objects.order_by('-date_joined')
	accounts = []
	for user in users:
		try:
			accounts.append(user.account)
		except ObjectDoesNotExist:
			continue

	return render(request, 'main/discover.html', {'accounts': accounts})

def feed(request, handle_name):
	userId = get_object_or_404(User, account=get_object_or_404(account, handle=handle_name))
	userAccount = userId.account
	try:
		image = userAccount.image_set.order_by('-date_uploaded')[0].identifier
	except IndexError:
		image = "5050.png"

	is_following = False

	if not request.user.is_authenticated:
		templateHTML = "main/feed.html"
		spitts = userAccount.spitt_set.order_by('-time_pub')
	elif request.user.pk == userId.pk:	
		templateHTML = "main/feed_my.html"
		spitts = userAccount.spitt_set.all()
		for pair in userAccount.follower_set.all():
			spitts = spitts | pair.followee.spitt_set.all()

		spitts = spitts.order_by('-time_pub')
	else:
		is_following = request.user.account.follower_set.filter(followee=userAccount).count() > 0
		spitts = userAccount.spitt_set.order_by('-time_pub')
		templateHTML = "main/feed.html"

	return render(request, templateHTML, {'user': userId, 'spitts': spitts, 'image': image, 'logged_as': request.user, 'is_following': is_following})

def feed_ajax_spitt(request, handle_name):
	if not request.user.is_authenticated or request.user.account.handle != handle_name:
		raise Http404("Invalid user operation, please log in!")

	userId = get_object_or_404(User, account=get_object_or_404(account, handle=handle_name))
	userAccount = userId.account
	try:
		image = userAccount.image_set.order_by('-date_uploaded')[0].identifier
	except IndexError:
		image = "5050.png"

	if request.method == "POST":
		form = SpittForm(request.POST)
		if form.is_valid():
			newSpitt = addNewSpitt(userAccount, form.cleaned_data['spittboxtext'])
			return render(request, 'main/feed_ajax_spitt.html', {'spitt': newSpitt, 'user': userId, 'image': image})
		else:
			return render(request, 'main/feed_ajax_spitt.html', {'error': True})
	else:
		return render(request, 'main/feed_ajax_spitt.html', {'error': True})

def feed_ajax_bio(request, handle_name):
	if not request.user.is_authenticated or request.user.account.handle != handle_name:
		raise Http404("Invalid user operation, please log in!")

	userId = get_object_or_404(User, account=get_object_or_404(account, handle=handle_name))
	userAccount = userId.account

	if request.method == "POST":
		form = BioForm(request.POST)
		if form.is_valid():
			updateAccountBio(userAccount, form.cleaned_data['userbio'])
			return render(request, 'main/feed_ajax_bio.html', {'bio': form.cleaned_data['userbio'].strip()})
		else:
			return render(request, 'main/feed_ajax_bio.html', {'error': True})
	else:
		return render(request, 'main/feed_ajax_bio.html', {'error': True})

def feed_ajax_img(request, handle_name):
	if not request.user.is_authenticated or request.user.account.handle != handle_name:
		raise Http404("Invalid user operation, please log in!")

	userId = get_object_or_404(User, account=get_object_or_404(account, handle=handle_name))
	userAccount = userId.account

	if request.method == "POST":
		form = ImgForm(request.POST, request.FILES)
		if form.is_valid():
			newImage = updateAccountImage(userAccount, request.FILES['imagefile'])
			return render(request, 'main/feed_ajax_img.html', {'img': reverse('getimage', args=(newImage.identifier,))})
		else:
			return render(request, 'main/feed_ajax_img.html', {'error': True})
	else:
		return render(request, 'main/feed_ajax_img.html', {'error': True})

def feed_ajax_follow(request, handle_name):
	if not request.user.is_authenticated:
		raise Http404("Invalid user operation, please log in!")

	followeeId = get_object_or_404(User, account=get_object_or_404(account, handle=handle_name))
	followeeAccount = followeeId.account
	followerAccount = request.user.account

	toggleFollowAccount(followerAccount, followeeAccount)

	return HttpResponse("Success")
		
