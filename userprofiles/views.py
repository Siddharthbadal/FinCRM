from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import UserProfile
from team.models import Team

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            team = Team.objects.create(name='The team name', created_by=request.user)
            team.member.add(request.user)
            team.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, 'userprofiles/signup.html',{
        'form':form
    })

@login_required
def myaccount(request):
    team = Team.objects.filter(created_by=request.user).first()
    return render(request, 'userprofiles/myaccount.html', {'team':team})