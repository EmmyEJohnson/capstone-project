from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.conf import settings
from django.http import JsonResponse
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from .forms import (
  VendorCreationForm, 
  VendorAuthForm, 
  VendorProfileForm
  )
from config.mixins import(
	AjaxFormMixin, 
	reCAPTCHAValidation,
	FormErrors,
	RedirectParams,
	)

# Create your views here.

# Global default messages
result = "Error"
message = "There was an error, please try again"

# Display vendor account page
class AccountView(TemplateView):
	template_name = "vendors/account.html"

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

# Allow vendors to update their profile
def profile_view(request):

	user = request.user
	vp = user.vendorprofile

	form = VendorProfileForm(instance = vp) 

	if request.is_ajax():
		form = VendorProfileForm(data = request.POST, instance = vp)
		if form.is_valid():
			obj = form.save()
			obj.has_profile = True
			obj.save()
			result = "Success"
			message = "Profile Updated"
		else:
			message = FormErrors(form)
		data = {'result': result, 'message': message}
		return JsonResponse(data)

	else:

		context = {'form': form}
		context['google_api_key'] = settings.GOOGLE_API_KEY
		context['base_country'] = settings.BASE_COUNTRY

		return render(request, 'vendors/profile.html', context)

# Vendor sign-up with reCapture security
class SignUpView(AjaxFormMixin, FormView):
	template_name = "vendors/sign_up.html"
	form_class = VendorCreationForm
	success_url = "/"

	#reCAPTURE key required in context
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["recaptcha_site_key"] = settings.RECAPTCHA_PUBLIC_KEY
		return context

	#Mixin logic to get, check and save reCAPTURE score
	def form_valid(self, form):
		response = super(AjaxFormMixin, self).form_valid(form)	
		if self.request.is_ajax():
			token = form.cleaned_data.get('token')
			captcha = reCAPTCHAValidation(token)
			if captcha["success"]:
				obj = form.save()
				obj.email = obj.username
				obj.save()
				up = obj.vendorprofile
				up.captcha_score = float(captcha["score"])
				up.save()
				
				login(self.request, obj, backend='django.contrib.auth.backends.ModelBackend')

				#change result & message on success
				result = "Success"
				message = "You have successfully signed up with Brewtiful San Diego"

				
			data = {'result': result, 'message': message}
			return JsonResponse(data)

		return response

# Vendor sign in/ login
class SignInView(AjaxFormMixin, FormView):

	template_name = "vendors/sign_in.html"
	form_class = VendorAuthForm
	success_url = "/"

	def form_valid(self, form):
		response = super(AjaxFormMixin, self).form_valid(form)	
		if self.request.is_ajax():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
   
			#Authenticate vendor
			user = authenticate(self.request, username=username, password=password)
			if user is not None:
				login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
				result = "Success"
				message = 'You are now logged in'
			else:
				message = FormErrors(form)
			data = {'result': result, 'message': message}
			return JsonResponse(data)
		return response



# Logout
def sign_out(request):

	logout(request)
	return redirect(reverse('vendors:sign-in'))
