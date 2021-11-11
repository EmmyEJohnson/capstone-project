from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.conf import settings
from django.http import JsonResponse
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator

# Create your views here.


from config.mixins import(
	AjaxFormMixin, 
	reCAPTCHAValidation,
	FormErrors,
	RedirectParams,
	)