from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Client
from .forms import AddClientForm, AddCommentForm
from team.models import Team

@login_required 
def add_client(request):
    team = Team.objects.filter(created_by=request.user).first()
    if request.method == 'POST':   
        form = AddClientForm(request.POST)

        if form.is_valid():
            team = Team.objects.filter(created_by=request.user).first()
            client = form.save(commit=False)
            client.created_by= request.user
            client.team = team
            client.save()
            messages.success(request, "Client Created!")

            return redirect('clients_list')

    else:
        form = AddClientForm()

    return render(request, 'client/add_client.html',
    {'form':form, 'team':team})


@login_required
def clients_list(request):
    clients = Client.objects.filter(created_by=request.user)
    return render(request, 'client/clients_list.html',
    {'clients':clients})


@login_required
def clients_detail(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    team = Team.objects.filter(created_by=request.user).first()

    if request.method == 'POST':
        form = AddCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.team = team 
            comment.created_by= request.user
            comment.client = client
            
            comment.save()

            return redirect("clients_detail",pk=pk)
    else:
        form= AddCommentForm()

    return render(request, 'client/clients_detail.html',{'client':client, 'form':form})


@login_required
def delete_client(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    client.delete()
    messages.success(request, "You deleted the Client!")
    return redirect('clients_list')


@login_required 
def edit_client(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)

    if request.method == 'POST':
        form = AddClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()

            messages.success(request, "Client details edited!")
            return redirect('clients_list')
    else:
        form = AddClientForm(instance=client)

    return render(request, 'client/edit_client.html',
    {'form':form})



