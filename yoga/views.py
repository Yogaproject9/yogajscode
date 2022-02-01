from django.test import TestCase

# Create your tests here.
from django.shortcuts import redirect, render, HttpResponseRedirect
from .forms import SignUpForm, ContactForm , LoginForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render
from django.http.response import StreamingHttpResponse
import cv2
from .yoga_ml import ml_function
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .models import *
from secrets import token_hex
import pytz
from datetime import datetime
from .liveFeed import VideoCamera
# from . camera import VideoCamera
# UserCreationForm :we get 3 fields username, pw1 and pw2(conformation)--bydefault
# Create your views here.


#---sign-up ---#
def sign_up(request):
    if request.method == 'POST':
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            messages.success(request, 'Congratulations! Account Created Successfully.')
            fm.save()
    else:
        fm = SignUpForm()
    return render(request, 'yoga/signform.html' , {'form': fm})


#--------login authentication------#

def user_login(request):
        if request.method == 'POST':
            fm = LoginForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upas = fm.cleaned_data['password']
                user= authenticate(username=uname, password=upas) #user obj created
                if user is not None:
                    login(request, user)
                    # messages.success(request, 'Login successfully Done')
                    return HttpResponseRedirect('/profile/')

        else:
            fm =LoginForm()
        return render(request, 'yoga/userlogin.html' , {'form': fm})


#----User profile--#
def user_profile(request):
    if request.user.is_authenticated:
        return render(request, 'yoga/profile.html' , {'name': request.user})
    else:
        return HttpResponseRedirect('/login/')


def video_feed(request):
    ml_function()
    return render(request, 'yoga/camera.html')


#---- Live Video Feed ----#

def test(request):
    return render(request, 'yoga/liveFeed.html')

def gen(camera):
    aasana=1
    while True:
        if(aasana==1):
            frame = camera.get_gray()
        if(frame[1]!=3):
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame[0] + b'\r\n\r\n')
        #     continue
        # aasana = 2
        # if(aasana == 2):
        #     frame = camera.get_gray()


def feed(request):
	return StreamingHttpResponse(gen(VideoCamera()),
                              content_type='multipart/x-mixed-replace; boundary=frame')






#--home page---#


def about(request):
    context = {'about':'active'}
    return render(request, 'yoga/about.html' , context)


#--classess---#
def classes(request):
    context = {'classes':'active'}
    return render(request, 'yoga/classes.html', context)

def index(request):
    return render(request,'yoga/index.html')

def beginner(request):
    return render(request, 'yoga/beginner.html')

def intermediate(request):
    return render(request, 'yoga/intermediate.html')

def advanced(request):
    return render(request, 'yoga/advanced.html')

def custom(request):
    return render(request, 'yoga/custom.html')

#---user logout--
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')
 

#---user change password with old pass--#
def user_changepass(request):
    if request.user.is_authenticated:
        if request.method =="POST":
            fm = PasswordChangeForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                messages.success(request, 'Password has been changed!')
                return HttpResponseRedirect('/login/')
        else:
            fm =PasswordChangeForm(user=request.user)
            
        return render(request, 'yoga/changepassword.html', {'form': fm})
    
    else:
        return HttpResponseRedirect('/login/')



#---Forgot password---#
def forgot_password(request):
    return render(request, 'yoga/forget_password.html')

def send_mail_forgot_password(request):
    if request.method =="POST":
        email=request.POST.get('email')

        try:    
            user_instance=User.objects.get(email=email)
        except User.DoesNotExist:
            messages.success(request, 'User does not exist!')
            return render(request, 'yoga/forget_password.html')
        
        UserToken.objects.filter(user=user_instance).delete()
        forgot_password_link="http://localhost:8000/reset_password_form"
        if user_instance.is_active:
            token=token_hex(16)
            user_token=UserToken.objects.create(user=user_instance,token=token)
            user_token.save()
            send_mail(
                    'Subject here',
                    'Your password reset link is ' +forgot_password_link+'?token='+token,
                    settings.FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
        
        else:
            messages.success(request, 'User is not active')
            return render(request, 'yoga/forget_password.html')
        
        messages.success(request, 'Password reset mail is succesfully sent')
        return render(request, 'yoga/forget_password.html')

#----Reset password---#
def reset_password_form(request):
    if request.method =="GET":
        global token
        token=request.GET.get('token')
        print(token)
    if request.method =="POST":
        # token=request.GET.get('token')
        password=request.POST.get('password')
        print(token)
        try:    
            user_token=UserToken.objects.get(token=token)
        except Exception as ObjectDoesNotExist:
            messages.success(request, 'Link is expired')
            return render(request, 'yoga/forgot_password_form.html')
        
        utc = pytz.utc
        current_time=datetime.now(tz=utc)
        diff=current_time-user_token.created_time
        total_seconds = diff.total_seconds()
        minutes = total_seconds/60
        
        if(minutes<=30):
            user_instance=user_token.user
            user_instance.set_password(password)
            user_instance.save()
            UserToken.objects.filter(user=user_instance).delete()

        else:
            UserToken.objects.filter(user=user_token.user).delete()
            messages.success(request, 'Link is expired')
            return render(request, 'yoga/forgot_password_form.html')
        
        messages.success(request, 'password successfully changed')
    return render(request, 'yoga/forgot_password_form.html')


#---FAQ---#

def faqpage(request):
    return render(request, 'yoga/faq.html')

#---contact page---#
def contactsendmsg(request):
    form = ContactForm(request.POST)
    if request.method=='POST':
       
        if form.is_valid():
            message = "Hi, \n PFB the user details:- \n \n Name-{} \n Email id - {} \n mobile number - {} \n message - {} \n Regards,".format(form.cleaned_data['Name'],form.cleaned_data['Email'],form.cleaned_data['Mobile'],form.cleaned_data['Message'])
            send_mail(
                    'Call back request',
                    message,
                    settings.FROM_EMAIL,
                    ['shivanids08@gmail.com'],
                    fail_silently=False,
                )
    else: 
        form = ContactForm()
    return render(request,'yoga/contact.html',{'form':form})


