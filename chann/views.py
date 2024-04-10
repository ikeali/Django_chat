from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from .forms import SignUpForm



def frontpage(request):
    return render(request, 'chann/frontpage.html')

def signup(request):
    if request.method =='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user= form.save()
            login(request, user)
            return redirect('frontpage')
        
    else:
        form = SignUpForm()
        
    return render(request,'chann/signup.html',{"form":form}) 


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('frontpage')
        else:
            return redirect(request,'signin',{'error':'Username or Password Invalid!'})
         
    return render(request,'chann/signin.html')  
        

def signout(request):
    logout(request)
    return redirect('frontpage')
    

    