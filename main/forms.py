from django import forms

from .models import account
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
	username = forms.CharField(label='Email Address', max_length=64)
	password = forms.CharField(widget=forms.PasswordInput, label='Password')

	def clean(self):
		cleaned_data = super(LoginForm, self).clean()
		username = cleaned_data.get("username")
		password = cleaned_data.get("password")

		if username and password and not authenticate(username=username, password=password):
			raise forms.ValidationError("Invalid username and/or password!")


class SignupForm(forms.Form):
	handle = forms.CharField(label='Display Name', max_length=18)
	username = forms.CharField(label='Email Address', max_length=64)
	password = forms.CharField(widget=forms.PasswordInput, label='Password')
	confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

	def clean(self):
		cleaned_data = super(SignupForm, self).clean()
		handle_data = cleaned_data.get("handle")
		pw = cleaned_data.get("password")
		pw_c = cleaned_data.get("confirm_password")
		email = cleaned_data.get("username")

		if handle_data and account.objects.filter(handle=handle_data).count() > 0:
			raise forms.ValidationError("Display name already exists!")

		if email and User.objects.filter(username=email).count() > 0:
			raise forms.ValidationError("Username already exists!")

		if len(pw) < 8:
			raise forms.ValidationError("Password must be at least 8 characters long!")

		if pw != pw_c:
			raise forms.ValidationError("Passwords do not match!")

class SpittForm(forms.Form):
	spittboxtext = forms.CharField(widget=forms.Textarea, max_length=150, min_length=1)

	def clean(self):
		cleaned_data = super(SpittForm, self).clean()
		cleaned_spittboxtext = cleaned_data.get('spittboxtext')
		if cleaned_spittboxtext and len(cleaned_spittboxtext.strip()) < 1:
			raise forms.ValidationError("Cannot be all spaces")

class BioForm(forms.Form):
	userbio = forms.CharField(widget=forms.Textarea, max_length=300, min_length=1)

	def clean(self):
		cleaned_data = super(BioForm, self).clean()
		cleaned_userbio = cleaned_data.get('userbio')
		if cleaned_userbio and len(cleaned_userbio.strip()) < 1:
			raise forms.ValidationError("Cannot be all spaces")


class ImgForm(forms.Form):
	imagefile = forms.ImageField()