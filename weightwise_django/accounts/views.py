from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import PatientSignUpForm


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome to WeightWise! Your patient account has been created.")
            return redirect('dashboard')
    else:
        form = PatientSignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})
