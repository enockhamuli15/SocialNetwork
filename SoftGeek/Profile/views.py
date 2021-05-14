from django.shortcuts import render, redirect, get_object_or_404
from SoftWord.models import Posts,Logins
from SoftWord.forms import PostForm 
from .forms import *
from .models import Profile, Relationship
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, UpdateView
from django.db.models import Q


# Create your views here.


@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    u_form = UserUpdateForm(request.POST, instance=request.user)
    p_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=profile)
    if request.method == 'POST':

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            
            # Get the current instance object to display in the template
            
            return redirect('profile')
       
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)
    
    context = {
                'p_form': p_form,
                'u_form': u_form,
                'profile': Profile.objects.get(user=request.user),
                'post_form': PostForm(),

                }   
    return render(request, 'profile_detail.html', context)



@login_required
def invites_received(request):
    profile = Profile.objects.get(user=request.user)
    query = Relationship.objects.invitations_received(profile)
    results = list(map(lambda x: x.sender, query))
    is_empty = False

    if len(results) == 0:
        is_empty = True

    context = {
        'query':results,
        'is_empty': is_empty,
        'profile': Profile.objects.get(user=request.user) 
        
    }
    return render(request, 'myInvites.html', context)
    


@login_required
def accept_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('my_invites')



@login_required
def reject_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('my_invites')



@login_required
def network_profiles_list(request):
    user = request.user
    query = Profile.objects.my_network(user)

    context = {
        'query':query,
        'profile': Profile.objects.get(user=request.user) 
    }
    return render(request, 'myNetwork.html', context)



@login_required
def profiles_list(request):
    user = request.user
    query = Profile.objects.get_all_profiles(user)

    context = {
        'query':query,
        'profile': Profile.objects.get(user=request.user) 
    }
    return render(request, 'listProfiles.html', context)


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'user_detail.html'

    def get_object(self, slug=None):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []

        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)  

        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['posts'] = self.get_object().get_all_authors_posts()
        context['len_posts'] = True if len(self.get_object().get_all_authors_posts()) > 0 else False
        
        return context



class ProfileListView(ListView):
    model = Profile
    template_name = 'listProfiles.html'
    context_object_name = 'query'

    def get_queryset(self):
        query = Profile.objects.get_all_profiles_to_invite(self.request.user)
        return query
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []

        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)  

        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context



@login_required
def send_invitations(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')
        
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profile')



@login_required
def remove_from_friends(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user =  request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get((Q(sender=sender) & Q(receiver=receiver))
            | (Q (sender=receiver) & Q(receiver=sender)))
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profile')        
