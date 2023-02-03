from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(request,
                                username=cleaned_data['username'],
                                password=cleaned_data['password'],
            )
            if user is not None and user.is_active:
                login(request, user)
                return HttpResponse('Authentication successful')
            else:
                return HttpResponse('Authentication failed')
            
        else:
            form = LoginForm()
        return render(request, 'templates/account/login.html', {'form': form})
                