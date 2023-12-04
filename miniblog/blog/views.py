from django.shortcuts import render,HttpResponseRedirect
from .forms import SignUpForm,LoginForm,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Post
from django.contrib.auth.models import Group

# Home:
def home(request):
    posts=Post.objects.all()
    return render(request,'blog/home.html',{'posts':posts})

#Queries:
# def queries(request):
    # user_profile = Post.objects.get(user=request.user)
    # context = {'user_profile': user_profile}
    # return render(request, 'blog/about.html', context)
    

#Contact:
def contact(request):
    return render(request,'blog/contact.html')

#dashboard:
def dashboard(request):
    if request.user.is_authenticated:
        posts=Post.objects.all()
        user=request.user
        full_name=user.get_full_name()
        gps=user.groups.all()
        return render(request,'blog/dashboard.html',{'posts':posts,'full_name':full_name,'groups':gps})
    else:
        return HttpResponseRedirect('/login/')
    
def profile(request):
    if request.user.is_authenticated:
        posts=Post.objects.all()
        user=request.user
        full_name=user.get_full_name()
        gps=user.groups.all()
        return render(request,'blog/profile.html',{'posts':posts,'full_name':full_name,'groups':gps})
    else:
        return HttpResponseRedirect('/login/')

#Logout:
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

#Signup:
def user_signup(request):
    if request.method=="POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,"Congratulations, Yoh have become an Author!")
            user=form.save()
            group=Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form=SignUpForm()
    return render(request,'blog/signup.html',{'form':form})

#Login:
def user_login(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            form=LoginForm(request=request,data=request.POST)
            if form.is_valid():
                uname=form.cleaned_data['username']
                pw=form.cleaned_data['password']
                user=authenticate(username=uname,password=pw)
                if user is not None:
                    login(request,user)
                    messages.success(request,"Logged In Successfully!!")
                    return HttpResponseRedirect('/dashboard/')
        else:
            form=LoginForm()
        return render(request,'blog/login.html',{'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')

#Add New Post:
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form=PostForm(request.POST)
            if form.is_valid():
                form.save()
                form=PostForm()
        else:
            form=PostForm()
        return render(request,'blog/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')
    
#Update Post:
def update_post(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi=Post.objects.get(pk=id)
            form=PostForm(request.POST,instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi=Post.objects.get(pk=id)
            form=PostForm(instance=pi)
        return render(request,'blog/updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')
    
#Delete Post:
def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi=Post.objects.get(pk=id)
            pi.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')