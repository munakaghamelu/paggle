from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == 'POST':
        # If we get a post request create a form with the requested data, else it's a GET so we just display a blank form
        form = UserCreationForm(request.POST)
        # need to check if authentication code is valid
        if form.is_valid():
            username = form.cleaned_data.get('username')
            # flash message to show we've received the data
            messages.success(request, f'Account created for {username}!')
            return redirect('paggle-selectTask')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})
