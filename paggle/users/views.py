from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
import os

# Create your views here.
def register(request):
    if request.method == 'POST':

        # If we get a post request create a form with the requested data, else it's a GET so we just display a blank form
        form = UserRegisterForm(request.POST)

        # need to check if authentication code is valid
        if form.is_valid():
            code = form.cleaned_data.get('code')
            validCode = False

            # need to change the path of this file and encrypt!
            pwd = os.path.dirname(__file__)
            with open(pwd + '/acceptable_codes') as f:
                for line in f:
                    if (code in line):
                        validCode = True

            if validCode:
                form.save()
                username = form.cleaned_data.get('username')
            
                # flash message to show we've received the data
                messages.success(request, f'Account created for {username}!')
                return redirect('paggle-selectTask')
            else:
                form = UserRegisterForm()
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
