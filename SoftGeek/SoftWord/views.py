from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import *
from Profile.forms import ProfileUpdateForm
from Profile.models import Profile
from .models import Posts,Like,Logins
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy



# Create your views here.

def home1(request):
    if request.method == 'POST':
        user = request.user
        form1 = PostForm(request.POST)
        
        if form1.is_valid():
            form1.save()

    context = {'home_posts': Posts.objects.all(),
               'form_post': PostForm(),
               'user': user,
                'profile': Profile.objects.get(user=request.user)
               }

    return render(request, 'home.html', context)



def domains(request):
    context = {'dom': Domains.objects.all()}
    return render(request, 'domains.html', context)

def notifications(request):
    return render(request, 'notifications.html')



def register(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():

            user = form.save()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            messages.success(request, f"Your account has been created successfully")
            return redirect('/')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = LoginForm()
        
        return render(request, 'register.html', {'form': form})




@login_required
def blog_post_like(request):
    
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Posts.objects.get(id=post_id)
        

        if user in post_obj.likes.all():
            post_obj.likes.remove(user)
        else:
            post_obj.likes.add(user)

        like, created = Like.objects.get_or_create(user=user, post_id=post_id)

        if not created:
            if like.value=='Like':
                like.value='Unlike'
            else:
                like.value='Like'
        else:
            like.value='Like'

        post_obj.save()
        like.save()

    return redirect('home_page')

@login_required
def post_comment_create_and_list_view(request):
    thisPost = Posts.objects.all()
    

    # initials
    p_form = PostForm()
    c_form = CommentModelForm()


    profile = Profile.objects.get(user=request.user)
    
    if 'submit_c_form' in request.POST:
        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Posts.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentModelForm()


    context = {

        'p_form': p_form,
        'c_form': c_form,
        'posts': thisPost,

    }

    return redirect('home_page')


class PostListView(ListView):
    
    model = Posts
    template_name = 'home.html'
    context_object_name = 'home_posts'
    extra_context = {
        "form": PostForm(),
        "c_form": CommentModelForm(),
        
        }
    ordering = ['-createdTime']


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Posts
    template_name = 'detail_post.html'
    


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Posts
    template_name = 'home.html'
    success_url = reverse_lazy('home_page')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        form.instance.author = profile
        return super().form_valid(form)

"""class CommentCreateView(LoginRequiredMixin, CreateView):
    form_class = CommentModelForm
    model = Comment
    template_name = 'home.html'
    context_object_name = 'c_form'
    extra_context = {'post_id'}
    success_url = reverse_lazy('home_page')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)"""

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = PostForm
    model = Posts
    template_name = 'update_posts.html'
    success_url = reverse_lazy('home_page')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)

        else:
            form.add_error(None, "You need to be the author of the post in order to update it")
            return super().form_invalid(form)

    def test_func(self):
        post = self.get_object()
        profile = Profile.objects.get(user=self.request.user)
        if profile == post.author:
            return True
        return False

