from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User


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
            # we set commit to false so we can change the role of the user and then save
            user = form.save(commit=False)
            user.role = User.COSTUMER
            user.save()
            return redirect('registerUser')
    else:
        form = UserForm()
    context = {'form': form}
    return render(request, 'accounts/registerUser.html', context)
