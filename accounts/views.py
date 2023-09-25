from django.shortcuts import render, redirect

from vendor.forms import VendorForm
from .forms import UserForm
from .models import User, userProfile
from django.contrib import messages, auth


def registerUser(request):
    """
        when we register a user in the form we actually saving an instance
        from the user model  which actually is the sender of the post_save
        so it will trigger the post_save function which creates a user profile
        linked to the user, because the form is actually a user instance
        that we are sending to the registerUser.html 
    """
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('dashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            """
            create a new user by using the form data directly
            """
            # we set commit to false so we can change the role of the user and then save
            # password = form.cleaned_data.get('password')
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.COSTUMER
            # user.save()
            
            """
            create a new user by using create_user method from the User model
            """
            first_name = form.cleaned_data.get('first_name')
            last_name  = form.cleaned_data.get('last_name')
            username   = form.cleaned_data.get('username')
            email      = form.cleaned_data.get('email')
            
            password = form.cleaned_data.get('password')
            
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
            )
            
            user.role = User.COSTUMER
            
            user.save()            
            messages.success(request, f"User {user.username} has been created successfully")
            
            return redirect('registerUser')
        else:
            print(f"form: {form.errors}")
    else:
        form = UserForm()
    context = {'form': form}
    return render(request, 'accounts/registerUser.html', context)

def registerVendor(request):
    
    """
        this function will create vendors, as the logic is like the pervious 
        but there are some issues for example we set the user form like the pervious
        and then we get receive them on two different form as vendor and user forms
        then after validating we create the user instance
        .............................................................................
        because we need the user first to create the vendor instance so we set the
        commit to false so we can set the user and then the user profile and others
        .............................................................................
        but we need the user profile as shown so we need to get the same userprofile
        as it is created instantly after user created (USING SIGNALS) 
    """
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('dashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name  = form.cleaned_data.get('last_name')
            username   = form.cleaned_data.get('username')
            email      = form.cleaned_data.get('email')
            
            password = form.cleaned_data.get('password')
            
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
            )
            
            user.role = User.VENDOR
            user.save()
            
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = userProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, "Your account has been created successfully, Please wait for the approval.")
            return redirect('registerVendor')
        else:
            print(f"form: {form.errors}")
    else:
         form = UserForm()
         v_form = VendorForm()

    context = {
            'form': form,
            'v_form': v_form,
    }
    return render(request, 'accounts/registerVendor.html', context=context)


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('dashboard')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are logged in successfully")
            return redirect('dashboard')
            
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
        
    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, "You are logged out successfully")
    return redirect('login')

def dashboard(request):
    return render(request, 'accounts/dashboard.html')