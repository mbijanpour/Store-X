from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User
from django.contrib import messages


def registerUser(request):
    """
        when we register a user in the form we actually saving an instance
        from the user model  which actually is the sender of the post_save
        so it will trigger the post_save function which creates a user profile
        linked to the user, because the form is actually a user instance
        that we are sending to the registerUser.html 
    """

    if request.method == 'POST':
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
            
            return redirect('registerUser')
        else:
            print(f"form: {form.errors}")
    else:
        form = UserForm()
    context = {'form': form}
    return render(request, 'accounts/registerUser.html', context)
