from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required


def register(request):
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # ^ saving our
            username = form.cleaned_data.get('username')
            # the validated data after the validation is stored now as username dict
            messages.success(request, f"Account created for {username}. Now you can login now!")
            return redirect('login')
    else:   
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == "POST":
        # populating the forms with the current user's info
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                   request.FILES, 
                                   instance=request.user.profile)
        # we have left the instances coz that has to know on which user we are changing
        # request.POST -> to pass in the post data 
        # request.FILES -> used coz we get the image file as well
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"The account has been updated!")
            return redirect('profile')
            # ^ sends a get request and avoids "Post Get Redirect Pattern"

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form':u_form,
        'p_form':p_form
    }

    return render(request, 'users/profile.html', context)

###############################
#  Different types of msg.s   #
#       messages.debug        #
#       messages.info         #
#       messages.success      #
#       messages.warning      #
#       messages.error        #
###############################