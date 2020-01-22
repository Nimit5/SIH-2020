from django.shortcuts import render,redirect
from django.http import HttpResponse
import math
from django.contrib import messages
import random
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User, auth
from . models import TribalUser, TribalSkills,Organisation,Apply_tribal_to_org,Invite_tribal_to_org
from PIL import Image
from .forms import Skill_Form
import requests as r
from bs4 import BeautifulSoup as bs


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
            orglist=getorganizationslist()
            return render(request,'tribal.html',{'email':email1, 'skill':skill,'first_skill':first_skill,'orglist':orglist})
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
    from django.utils import translation
    if translation.LANGUAGE_SESSION_KEY in request.session:
        del request.session[translation.LANGUAGE_SESSION_KEY]
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
            user_log_in_tribal=TribalUser.objects.filter(email=email1)
            user_log_in_org=TribalUser.objects.filter(email=email1)
            if(len(user_log_in_tribal)==0):
                triballist=gettribalslist()
                usershow=getuser(triballist)
                print('inside- ',usershow)
                return render(request,'orgs.html',{'tl':triballist,'usershow':usershow})
            else:
                skill=getskills(email1)
                first_skill=skill[0]
                skill=skill[1:]
                orglist=getorganizationslist()
                return render(request,'tribal.html',{'email':email1, 'skill':skill,'first_skill':first_skill,'orglist':orglist})
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
                
                print(email)
                print(phone)
                print(orgname)
                userorg=Organisation(email=email,desc=' ',mobile=phone, org_name=orgname)
                userorg.save()
                user.save()
                user = auth.authenticate(username=email,password=password)
                auth.login(request, user)
                triballist=gettribalslist()
                usershow=getuser(triballist)
                print('inside- ',usershow)
                return render(request,'orgs.html',{'tl':triballist,'usershow':usershow})
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
        orglist=getorganizationslist()
        return render(request,'tribal.html',{'email':email1, 'skill':skill,'first_skill':first_skill,'orglist':orglist})
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
            triballist=gettribalslist()
            usershow=getuser(triballist)
            print('inside- ',usershow)
            return render(request,'orgs.html',{'tl':triballist,'usershow':usershow})
        else:
            skill=getskills(email1)
            first_skill=skill[0]
            skill=skill[1:]
            orglist=getorganizationslist()
            return render(request,'tribal.html',{'email':email1, 'skill':skill,'first_skill':first_skill,'orglist':orglist})
    else:
        return render(request,'index.html',{'n':True})


def apply(request,myid):
    print('hello i am here')
    org_detail=Organisation.objects.filter(id=myid)
    email=request.user.get_username()
    print(org_detail)
    name=request.user.get_full_name()
    my_detail= TribalUser.objects.filter(email=email)
    s=[]
    skill=getskills(email)
    for i in skill:
        s.append(i.title)
    return render(request,'apply.html',{'org_detail':org_detail[0],'my_detail':my_detail[0], 'name':name,'skill':s})

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

def getorganizationslist():
    org=Organisation.objects.all()
    return org

def gettribalslist():
    trib=TribalUser.objects.all()
    print(trib)
    return trib

def makeapplication(request):
    if request.method=='POST':
        org_email=request.POST.get('email','')
        tribalemail=request.user.get_username()
        application=request.POST.get('application','')
        appl=Apply_tribal_to_org(tribalemail=tribalemail,orgemail=org_email,application=application,status='requested')
        appl.save()
        skill=getskills(tribalemail)
        first_skill=skill[0]
        skill=skill[1:]
        orglist=getorganizationslist()
        return render(request,'tribal.html',{'email':tribalemail, 'skill':skill,'first_skill':first_skill,'orglist':orglist})



def getuser(triballist):
    s=[]
    for i in triballist:
        use=User.objects.filter(username=i.email)
        s.append(use)
    print('inside')
    return s

def invite(request,myid):
    usertribalinfo=User.objects.filter(id=myid)
    email=request.user.get_username()

    print('hello- ',email)
    userorg=Organisation.objects.filter(email=email)
    print(usertribalinfo)
    print(userorg)
    return render(request,'invite.html',{'usertribal':usertribalinfo[0],'userorg':userorg[0]})

def makeinvitation(request):
    if request.method=='POST':
        tribal_email=request.POST.get('email','')
        orgemail=request.user.get_username()
        application=request.POST.get('application','')
        appl=Invite_tribal_to_org(tribalemail=tribal_email,orgemail=orgemail,application=application,status='requested')
        appl.save()
        triballist=gettribalslist()
        usershow=getuser(triballist)
        print('inside- ',usershow)
        return render(request,'orgs.html',{'tl':triballist,'usershow':usershow})

def invitation(request):
    email=request.user.get_username()
    myrequest=Invite_tribal_to_org.objects.filter(tribalemail=email)
    org_name=[]
    for i in myrequest:
        ob=Organisation.objects.filter(email=i.orgemail)
        name=ob[0].org_name
        org_name.append(name)

    return render(request,'Receivedinvitation.html',{'my':org_name})

def myrequests(request):
    email=request.user.get_username()
    myrequest=Apply_tribal_to_org.objects.filter(tribalemail=email)
    org_name=[]
    for i in myrequest:
        ob=Organisation.objects.filter(email=i.orgemail)
        name=ob[0].org_name
        org_name.append(name)
    l=list(range(len(org_name)))
    print(org_name)
    s=[]
    skill=getskills(email)
    for i in skill:
        s.append(i.title)
    print(s)
    sk=''
    for x in s:
        sk=sk+x+','
    print(sk)
    sk=sk[0:31] 
    
    return render(request,'sentRequest.html',{'my':org_name,'skill':sk})

def scheme(request):
    url="https://tribal.nic.in/Schemes.aspx"
    response = r.get(url)
    soup = bs(response.text, "html.parser")

    main_box = soup.find_all("ul",{"class":"list"})

    scheme_heading = []
    link_name=[]
    link_url=[]
    x={}
    y={}
    lister_size_ranger=[]
    for i in range(1,len(main_box)):
        scheme_heading.append(main_box[i].find('strong').text)
        l= main_box[i].find_all('li')
        
        data=[]
        link=[]
        
        lister_size_ranger.append(list(range(len(l))))
        
        for j in range(len(l)):
            data.append(l[j].text)
            link.append('https://tribal.nic.in/'+(l[j].find('a').get('href')))
            y[l[j].text]='https://tribal.nic.in/'+(l[j].find('a').get('href'))
        link_name.append(data)
        link_url.append(link)
        
        x[main_box[i].find('strong').text]=link_name[i-1]
    sizer=len(scheme_heading)
    print(x)
    print(lister_size_ranger)
    return render(request,'schemes.html',{'y':y,'sizer':range(sizer),'lister_size_ranger':lister_size_ranger,'scheme_heading':scheme_heading,'link_name':link_name,'link_url':link_url,'x':x})


def viewrequest(request):
    email=request.user.get_username()
    view_requests=Apply_tribal_to_org.objects.filter(orgemail=email)
    tribal_name=[]
    tribal_skill=[]
    for i in view_requests:
        ob=User.objects.filter(username=i.tribalemail)
        name=ob[0].first_name
        s=[]
        skill=getskills(ob[0].username)
        for i in skill:
            s.append(i.title)
        sk=''
        for x in s:
            sk=sk+x+','
        sk=sk[0:31]
        tribal_skill.append(sk)

        tribal_name.append(name)
    print(len(tribal_skill))
    print(len(tribal_name))
    return render(request,'Receivedrequest.html', {'recieved_requests':tribal_name,'len':list(range(len(tribal_name))),'tribalskill':tribal_skill})

def sendinvitationoforg(request):
    email=request.user.get_username()
    view_invitation=Invite_tribal_to_org.objects.filter(orgemail=email)
    return render(request,'sentInvitations.html', {'view_invitation':view_invitation})

def viewskill(request):
    email=request.user.get_username()
    skill=getskills(email)
    first_skill=skill[0]
    skill=skill[1:]
    orglist=getorganizationslist()
    return render(request,'editskills.html',{'email':email,'skill':skill,'first_skill':first_skill})