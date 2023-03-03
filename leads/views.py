from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, View
from django.urls import reverse_lazy

from .models import Lead 
from team.models import Team
from .forms import AddLeadForm, AddCommentForm
from client.models import Client


class LeadListView(ListView):
    model = Lead

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self):
        queryset = super(LeadListView, self).get_queryset()
        queryset = queryset.filter(created_by=self.request.user, converted_to_client=False)

        return queryset 



class LeadCreateView(CreateView):
    model = Lead
    fields = ('name', 'email', 'description','priority','status')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = Team.objects.filter(created_by=self.request.user).first()
        context['team'] = team 
        context['title'] = 'Add Lead'
        return context
    
    def get_success_url(self):
        return reverse_lazy('leads:list')
    
    def form_valid(self, form):
        team = Team.objects.filter(created_by=self.request.user).first()

        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.team = team 
        self.object.save()
        messages.success(self.request, "Lead Created!")
        return redirect(self.get_success_url())



class LeadDetailView(DetailView):
    model = Lead

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddCommentForm
        return context

    def get_queryset(self):
        queryset = super(LeadDetailView, self).get_queryset()
        queryset= queryset.filter(created_by=self.request.user, pk=self.kwargs.get("pk"))  
        return queryset





class LeadDeleteView(DeleteView):
    model = Lead
    success_url = reverse_lazy('leads:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self):
        queryset = super(LeadDeleteView, self).get_queryset()
        queryset = queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))
        messages.success(self.request, "Lead deleted!")
        return queryset
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    

class AddCommentView(View):
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        print(pk)
        contect = request.POST.get('content')
        print(contect)
        
        form = AddCommentForm(request.POST)
        if form.is_valid():
            team = Team.objects.filter(created_by=self.request.user).first()
            comment = form.save(commit=False)
            comment.team =team 
            comment.created_by=request.user 
            comment.lead_id = pk 
            comment.save()

        return redirect("leads:detail", pk=pk)


class LeadUpdateView(UpdateView):
    model = Lead 
    fields = ('name', 'email', 'description','priority','status')
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Lead'
        return context
    
    def get_queryset(self):
        queryset = super(LeadUpdateView, self).get_queryset()
        queryset = queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))
        
        return queryset
    
    def get_success_url(self) -> str:
        messages.success(self.request, "Lead updated!")
        return reverse_lazy('leads:list')



class ConvertToClient(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
        team = Team.objects.filter(created_by=request.user).first()

        client = Client.objects.create(name=lead.name, email=lead.email, description=lead.description, created_by=request.user, team=team)

        lead.converted_to_client=True 
        lead.save()
        messages.success(request, "Lead converted in to a client!")
        return redirect('leads:list')






"""
@login_required
def convert_to_client(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    team = Team.objects.filter(created_by=request.user)[0]

    client = Client.objects.create(name=lead.name, email=lead.email, description=lead.description, created_by=request.user, team=team)

    lead.converted_to_client=True 
    lead.save()
    messages.success(request, "Lead converted in to a client!")
    return redirect('leads:list')

"""




"""
@login_required 
def add_lead(request):
    team = Team.objects.filter(created_by=request.user)[0]

    if request.method == 'POST':   
        form = AddLeadForm(request.POST)

        if form.is_valid():
            team = Team.objects.filter(created_by=request.user)[0]
            lead = form.save(commit=False)
            lead.created_by= request.user
            lead.team = team
            lead.save()

            messages.success(request, "Lead Created!")

            return redirect('dashboard:index')

    else:
        form = AddLeadForm()

    return render(request, 'leads/add_lead.html',
    {'form':form, 'team':team})

"""



# @login_required 
# def edit_lead(request, pk):
#     lead = get_object_or_404(Lead, created_by=request.user, pk=pk)

#     if request.method == 'POST':
#         form = AddLeadForm(request.POST, instance=lead)
#         if form.is_valid():
#             form.save()

#             messages.success(request, "Lead details edited!")
#             return redirect('leads:list')
#     else:
#         form = AddLeadForm(instance=lead)

#     return render(request, 'leads/edit_lead.html',
#     {'form':form})



# @login_required
# def lead_delete(request, pk):
#     lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
#     lead.delete()
#     messages.success(request, "Lead deleted!")
#     return redirect('leads:list')


# @login_required
# def leads_detail(request, pk):
#     lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
#     # lead = Lead.objects.filter(created_by=request.user).get(pk=pk)

    

#     return render(request, 'leads/lead_detail.html', {
#         'lead':lead,
#     })


# @login_required
# def leads_list(request):
#     leads = Lead.objects.filter(created_by=request.user, converted_to_client=False)

#     return render(request, 'leads/lead_list.html',
#     {'leads':leads})