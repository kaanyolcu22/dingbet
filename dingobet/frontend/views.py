from django.shortcuts import render

# Create your views here.
# frontend/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to a home page or another page
    else:
        form = AuthenticationForm()
    return render(request, 'frontend/login.html', {'form': form})


def home_view(request):
    return render(request, 'frontend/home.html')

