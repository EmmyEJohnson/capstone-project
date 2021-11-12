from django.urls import path
from . import views

app_name = "vendors"

urlpatterns = [
  path('', views.AccountView.as_view(), name="vendor_account"),
	path('vendor_profile', views.ProfileView, name="vendor_profile"),
	path('vendor_sign_up', views.SignUpView.as_view(), name="vendor_sign_up"),
	path('vendor_sign_in', views.SignInView.as_view(), name="vendor_sign_in"),
	path('vendor_sign_out', views.SignOut, name="vendor_sign_out"),
]