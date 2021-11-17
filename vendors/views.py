from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Vendor
from inventory.models import BrewProduct, BrewProductImage
from .forms import BrewProductForm, BrewProductImageForm
from django.utils.text import slugify

# Create your views here.
def create_vendor(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            vendor = Vendor.objects.create(name=user.username, created_at=user)

            return redirect('frontpage')
    else:
        form = UserCreationForm()

    return render(request, 'vendor/create_vendor.html', {'form': form})

@login_required
def vendor_admin(request):
    vendor = request.user.vendor
    products = vendor.products.all()
    orders = vendor.orders.all()

    for order in orders:
        order.vendor_amount = 0
        order.vendor_paid_amount = 0
        order.fully_paid = True

        for item in order.items.all():
            if item.vendor == request.user.vendor:
                if item.vendor_paid:
                    order.vendor_paid_amount += item.get_total_price()
                else:
                    order.vendor_amount += item.get_total_price()
                    order.fully_paid = False

    return render(request, 'vendor/vendor_admin.html', {'vendor': vendor, 'products': products, 'orders': orders})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = BrewProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user.vendor
            product.slug = slugify(product.title)
            product.save()

            return redirect('vendor_admin')
    else:
        form = BrewProductForm()
    
    return render(request, 'vendor/add_product.html', {'form': form})

@login_required
def edit_product(request, pk):
    vendor = request.user.vendor
    brewproduct = vendor.products.get(pk=pk)

    if request.method == 'POST':
        form = BrewProductForm(request.POST, request.FILES, instance=brewproduct)
        image_form = BrewProductImageForm(request.POST, request.FILES)

        if image_form.is_valid():
            brewproductimage = image_form.save(commit=False)
            brewproductimage.product = brewproduct
            brewproductimage.save()

            return redirect('vendor_admin')

        if form.is_valid():
            form.save()

            return redirect('vendor_admin')
    else:
        form = BrewProductForm(instance=brewproduct)
        image_form = BrewProductImageForm()
    
    return render(request, 'vendor/edit_product.html', {'form': form, 'image_form': image_form, 'brewproduct': brewproduct})

@login_required
def edit_vendor(request):
    vendor = request.user.vendor

    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')

        if name:
            vendor.created_by.email = email
            vendor.created_by.save()

            vendor.name = name
            vendor.save()

            return redirect('vendor_admin')
    
    return render(request, 'vendor/edit_vendor.html', {'vendor': vendor})

def vendors(request):
    vendors = Vendor.objects.all()

    return render(request, 'vendor/vendors.html', {'vendors': vendors})

def vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)

    return render(request, 'vendor/vendor.html', {'vendor': vendor})








# class VendorHome(TemplateView):
#     template_name = "vendors/vendor_home.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["signupform"] = CustomUserCreationForm()
#         context["loginform"] = LoginForm()
#         return context

# class Login(View):
    
#     def get(self, request):
#         form = LoginForm()
#         signupform = CustomUserCreationForm()
#         context = {"loginform": form, "signupform": signupform}
#         return render(request, "vendors/registration/login.html", context)
    
#     def post(self, request):
#         username = request.POST['username']
#         password = request.POST['password1']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('vendors/vendor_profile', pk=user.id)
#         else:
#             form = LoginForm()
#             signupform = CustomUserCreationForm()
#             error = "Invalid Credentials" 
#             context = {"loginform": form, "signupform": signupform, "error": error}
#             return render(request, "vendors/registration/login.html", context)
          
          
# class Signup(View):
    
#     def get(self, request):
#         loginform = LoginForm()
#         form = CustomUserCreationForm()
#         context = {"signupform": form, "loginform": loginform}
#         return render(request, "vendors/registration/signup.html", context)
    
#     def post(self, request):
#         form = CustomUserCreationForm(request.POST)

#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('vendors/vendor_profile', pk=self.request.user.pk)
#         else:
#             loginform = LoginForm()
#             context = {"signupform": form, "loginform": loginform}
#             return render(request, "vendors/registration/signup.html", context)
          
          
# class VendorProfilePage(TemplateView):
#     model = VendorProfile
#     template_name = "vendors/vendor_profile.html"
#     ordering = ['created_at']

#     def get_context_data(self, pk, **kwargs):
#         vendor_profile = VendorProfile.objects.get(pk=pk)
#         context = super().get_context_data(**kwargs)
#         context["vendor_profile"] = vendor_profile
#         context["posts"] = vendor_profile.post.all().order_by('-created_at')
#         return context


# class VendorProfileUpdate(UpdateView):
#     model = User
#     form_class = VendorProfileForm
#     template_name = "vendors/vendor_profile_update.html"
    
#     def get_success_url(self):
#         return reverse('vendors/vendor_profile', kwargs={'pk': self.object.pk})


# class VendorProfilePictureUpdate(UpdateView):
#     model = VendorProfile
#     form_class = VendorProfilePictureForm
#     template_name = "vendors/vendor_profile_picture_update.html"
    
#     def get_success_url(self):
#         return reverse('vendors/vendor_profile', kwargs={'pk': self.object.pk})

# class PostDetail(DetailView):
#     model = PostInventory
#     template_name = "vendors/vendor_post_details.html"
    
# class BrewList(TemplateView):
#     template_name = "brew_list.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         name = self.request.GET.get("brew_type")

#         if name != None:
#             context["brews"] = Brew.objects.filter(name__icontains=name)
#         else:
#             context["brews"] = Brew.objects.all()
#         return context
      
# class BrewDetail(TemplateView):
#     template_name = "vendor_brew_details.html"

#     def get_context_data(self, pk, **kwargs):
#         context = super().get_context_data(**kwargs)
#         name = self.request.GET.get("brew_type")

#         if name != None:
#             context["brews"] = Brew.objects.filter(name__icontains=name)
#             context["brew_details"] = Brew.objects.get(pk=pk)
#         else:
#             context["brews"] = Brew.objects.all()
#             context["brew_details"] = Brew.objects.get(pk=pk)
#         return context      
      

# class VendorProfilePostCreate(CreateView):
#     model = PostInventory
#     fields = ['title', 'description', 'image']
#     template_name = "vendors/vendor_profile_post_create.html"

#     def form_valid(self, form, **kwargs):
#         form.instance.vendor_profile = self.request.user.vendor_profile
#         return super(VendorProfilePostCreate, self).form_valid(form)

#     def get_success_url(self):
#         return reverse('vendors/vendor_profile', kwargs={'pk': self.kwargs.get('pk')})

# class VendorProfilePostUpdate(UpdateView):
#     model = PostInventory
#     fields = ['title', 'description', 'image']
#     template_name = "vendors/vendor_post_update.html"

#     def form_valid(self, form, **kwargs):
#         form.instance.profile = self.request.user.vendor_profile
#         return super(VendorProfilePostUpdate, self).form_valid(form)

#     def get_success_url(self, **kwargs):
#         return reverse('vendors/vendor_profile', kwargs={'pk': self.request.user.pk})
      
# class VendorProfilePostDelete(DeleteView):
#     model = PostInventory
#     template_name = "vendors/vendor_profile_post_delete_confirmation.html"
    
#     def get_success_url(self):
#         return reverse('vendors/vendor_profile', kwargs={'pk': self.request.user.pk})
      
# class BrewPostCreate(CreateView):
#     model = Brew
#     fields = ['title', 'description', 'image']
#     template_name = "brew_post_create.html"

#     def form_valid(self, form, **kwargs):
#         form.instance.profile = self.request.user.profile
#         form.instance.brew = Brew.objects.get(pk=self.kwargs['pk'])
#         return super(BrewPostCreate, self).form_valid(form)
    
#     def get_absolute_url(self):
#       return reverse('brew_detail', kwargs={'pk': self.pk})

# class BrewPostUpdate(UpdateView):
    
#     model = Brew
#     fields = ['title', 'description', 'image']
#     template_name = "brew_post_update.html"
    
#     def get_success_url(self):
#         return reverse('brew_detail', kwargs={'pk': self.kwargs.get('brew_pk')})

# class BrewPostDelete(DeleteView):
#     model = Brew
#     template_name = "brew_post_delete_confirmation.html"
    
#     def get_success_url(self):
#         return reverse('brew_detail', kwargs={'pk': self.kwargs.get('brew_pk')})






# # # Global default messages
# # result = "Error"
# # message = "There was an error, please try again"


# # Display vendor account page
# class AccountView(TemplateView):
# 	template_name = "vendors/vendor_account.html"

# 	@method_decorator(login_required)
# 	def dispatch(self, *args, **kwargs):
# 		return super().dispatch(*args, **kwargs)


# # Function based view allows vendors to update profile
# def ProfileView(request):

# 	user = request.user
# 	vp = user.vendorprofile
# 	form = VendorProfileForm(instance = vp) 
# 	result = "Success"
# 	message = "Profile Updated"

# 	if request.is_ajax():
# 				form = VendorProfileForm(data = request.POST, instance = vp)
# 				if form.is_valid():
# 						obj = form.save()
# 						obj.has_profile = True
# 						obj.save()
# 				else:
# 						message = FormErrors(form)
# 				data = {'result': result, 'message': message}
# 				return JsonResponse(data)

# 	else:
# 				context = {'form': form}
# 				context['google_api_key'] = settings.GOOGLE_API_KEY
# 				context['base_country'] = settings.BASE_COUNTRY
# 				return render(request, 'vendors/vendor_profile.html', context)


# # Vendor sign-up with reCapture security
# class SignUpView(AjaxFormMixin, FormView):
# 	template_name = "vendors/vendor_sign_up.html"
# 	form_class = CustomUserCreationForm
# 	success_url = "/"


# 	#reCAPTURE key required in context
# 	def get_context_data(self, **kwargs):
# 					context = super().get_context_data(**kwargs)
# 					context["recaptcha_site_key"] = settings.RECAPTCHA_KEY
# 					return context


# 	#Mixin logic to get, check and save reCAPTURE score
# 	def form_valid(self, form):
# 		response = super(AjaxFormMixin, self).form_valid(form)	
# 		if self.request.is_ajax():
# 			token = form.cleaned_data.get('token')
# 			captcha = reCAPTCHAValidation(token)
# 			if captcha["success"]:
# 				obj = form.save()
# 				obj.email = obj.username
# 				obj.save()
# 				up = obj.vendorprofile
# 				up.captcha_score = float(captcha["score"])
# 				up.save()
				
# 				login(self.request, obj, backend='django.contrib.auth.backends.ModelBackend')

# 				#change result & message on success
# 				result = "Success"
# 				message = "You have successfully signed up with Brewtiful San Diego"
	
# 			data = {'result': result, 'message': message}
# 			return JsonResponse(data)

# 		return response


# # Vendor sign in/ login
# class SignInView(AjaxFormMixin, FormView):

# 	template_name = "vendors/vendor_sign_in.html"
# 	form_class = LoginForm
# 	success_url = "/"

# 	def form_valid(self, form):
# 					response = super(AjaxFormMixin, self).form_valid(form)	
# 					if self.request.is_ajax():
# 									username = form.cleaned_data.get('username')
# 									password = form.cleaned_data.get('password')
   
# 									#Authenticate vendor
# 									user = authenticate(self.request, username=username, password=password)
# 									if user is not None:
# 													login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
# 													result = "Success"
# 													message = 'You are now logged in'
# 									else:
# 													message = FormErrors(form)
# 									data = {'result': result, 'message': message}
# 									return JsonResponse(data)
# 					return response
   

# # Function based view for logout/ sign out
# def SignOut(request):

# 		logout(request)
# 		return redirect(reverse('vendors:vendor_sign_in'))


