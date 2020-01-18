from django.shortcuts import render,redirect
from django.http import HttpResponse
import math
from django.contrib import messages
import random
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User, auth
from . models import TribalUser, TribalSkills,Organisation
from PIL import Image
from .forms import Skill_Form

IMAGE_FILE_TYPES= ['png','jpg','jpeg']

def uploadskill(request):
    form=Skill_Form()
    email1=request.POST.get('email')
    print('inside uploadskill')
    print(email1)
    if request.method=='POST':
        form=Skill_Form(request.POST,request.FILES)
        if form.is_valid():
            user_pr=form.save(commit=False)
            user_pr.img=request.FILES['myFile']
            user_pr.title=request.POST.get('title')
            user_pr.desc=request.POST.get('desc')
            user_pr.email=request.POST.get('email')
            file_type= user_pr.img.url.split('.')[-1]
            file_type=file_type.lower()
            
            if file_type not in IMAGE_FILE_TYPES:
                return HttpResponse('file format not found')
            user_pr.save()
            skill=getskills(email1)
            first_skill=skill[0]
            skill=skill[1:]
            return render(request,'tribal.html',{'email':email1, 'skill':skill,'first_skill':first_skill})
        else:
            return HttpResponse('hello inside')
    else:
        return HttpResponse('hello')

def logout(request):
    if request.user.is_authenticated:
        print('login')
    else:
        print('logout')
    
    auth.logout(request)
    if request.user.is_authenticated:
        print('login')
    else:
        print('logout')
    
    return redirect('/')

def index(request):
    if request.method=='POST':
        email=request.POST.get('email','')
        name=request.POST.get('name','')
        phone=request.POST.get('mobile','')
        password=request.POST.get('password','')
        confirmpassword=request.POST.get('confpassword','')
        if(password==confirmpassword):
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return render(request,'index.html',{'passmiss':True})
            else:
                otp=generateOTP()
                category=request.POST.get('category','')
                s=[email,name,phone,password,otp,category]
                reciepents=[]
                reciepents.append(email)
                message='Your otp for the app is '+otp
                x=send_mail('Aakriti Authentication',message,'aakrati.foundation2020@gmail.com',reciepents,fail_silently=False,)
                print(x)

                if(x==1):
                    return render(request,'indexotp.html',{'userdata':s,'n':False,'passmiss':False})
                else:
                    return HttpResponse('hello how are you')
        else:
            messages.info(request,'password mismatch')
            return render(request,'index.html',{'passmiss':True})
    else:
        if request.user.is_authenticated:
            email1=request.user.get_username()
            skill=getskills(email1)
            first_skill=skill[0]
            skill=skill[1:]
            return render(request,'tribal.html',{'email':email1, 'skill':skill,'first_skill':first_skill})
        else:
            return render(request,'index.html',{'n':False})

def registerorg(request):
    if request.method=='POST':
        email=request.POST.get('email','')
        name=request.POST.get('name','')
        phone=request.POST.get('mobile','')
        password=request.POST.get('password','')
        confirmpassword=request.POST.get('confpassword','')
        orgname=request.POST.get('orgname','')
        if(password==confirmpassword):
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return render(request,'index.html',{'passmiss':True})
            else:
                user =User.objects.create_user(username=email,password=password,email=email,first_name=name)
                user.save()
                print(email)
                print(phone)
                print(orgname)
                userorg=Organisation(email=email,desc=' ',mobile=phone, org_name=orgname)
                userorg.save()
                user = auth.authenticate(username=email,password=password)
                auth.login(request, user)
                return render(request,'orgs.html')
        else:
            messages.info(request,'password mismatch')
            return render(request,'index.html',{'passmiss':True})




def generateOTP() :   
    string = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    OTP = "" 
    length = len(string) 
    for i in range(6) : 
        OTP += string[math.floor(random.random() * length)] 
    return OTP 

def verifyotp(request):
    a=request.POST.get('userdata_hidden','')
    x=[]
    k=a[1:(len(a)-1)]
    k=k.replace(" ", "")
    k=k.replace("'", "")
    p=k.split(',')
    email=p[0]
    name=p[1]
    phone=p[2]
    password=p[3]
    
    actual_otp=p[4]
    category=p[5]
    enter_otp=request.POST.get('OTP','')
    if(enter_otp==actual_otp):
        user =User.objects.create_user(username=email,password=password,email=email,first_name=name)
        user.save()
        user = auth.authenticate(username=email,password=password)
        auth.login(request, user)
        user1=TribalUser(email=email,type_user='Tribal',mobile=phone,category=category)
        user1.save()
        email1=request.user.get_username()
        skill=getskills(email1)
        first_skill=skill[0]
        skill=skill[1:]
        return render(request,'tribal.html',{'email':email1, 'skill':skill,'first_skill':first_skill})
    else:
        return render(request,'indexotp.html',{'userdata':a,'n':True})

def login(request):
    email=request.POST.get('Mobile num.','')
    password=request.POST.get('passwordinput.','')
    
    user = auth.authenticate(username=email,password=password)    
    if user is not None:

        auth.login(request, user)
        email1=request.user.get_username()
        user_log_in_tribal=TribalUser.objects.filter(email=email1)
        user_log_in_org=TribalUser.objects.filter(email=email1)
        if(len(user_log_in_tribal)==0):
            return render(request,'orgs.html')
        else:
            skill=getskills(email1)
            first_skill=skill[0]
            skill=skill[1:]
            return render(request,'tribal.html',{'email':email1, 'skill':skill,'first_skill':first_skill})
    else:
        return render(request,'index.html',{'n':True})


def apply(request):
    return render(request,'apply.html')

def getskills(email1):
    skill=[]
    skill1=TribalSkills.objects.all()
    for item in skill1:
        if item.email==email1:
            skill.append(item)
    print(skill)
    return skill
            

def show_skill(request,myid):
    skill_detail = TribalSkills.objects.filter(id=myid)
    print(skill_detail)
    return render(request,'show_skill_detail.html',{'skill_detail':skill_detail[0]})

def show_profile_tribal(request):
    username=request.user.get_username()
    email=request.user.get_username()
    name=request.user.get_full_name()
    tribaluser=TribalUser.objects.filter(email=email)
    phone=tribaluser[0].mobile
    category=tribaluser[0].category
    s=[]
    skill=getskills(email)
    for i in skill:
        s.append(i.title)
    
    return render(request,'MyProfile.html',{'email':email,'name':name,'phone':phone,'category':category,'skill':s})

def orgProfile(request):
    return render(request,'orgProfile.html')

def contactorg(request):
    return render(request,'contact.html')

