from distutils.log import error
from email import message
import urllib.parse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.timezone import now
from .filters import *
from .forms import *
from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile,TemporaryUploadedFile
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import pandas as pd
from django.core.cache import cache
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv
# Create your views here.
# Create your views here.
def home(request):
    FrontContents = FrontPage.objects.all()
    Galleries = Gallery.objects.all()
    TaeNews = News.objects.all()
    Contents= Content.objects.all()
    SampleNews = TaeNews[0:4]
    images = Galleries[1:8]
    return render(request, 'home.html',{'Contents':Contents,'FrontContents':FrontContents,'Galleries':images, 'News':SampleNews})    

def publicGallery(request):
    Galleries = Gallery.objects.all()
    return render(request, 'TAEApp/public/publicGallery.html',{'Galleries':Galleries})  

def AboutMember(request):
    return render(request, 'TAEApp/public/AboutMember.html')  

def Leadership(request):
    return render(request, 'TAEApp/public/Leadership.html')  

def AboutElection(request):
    return render(request, 'TAEApp/public/AboutElection.html') 

def ObtainMemberID(request):
    if request.method == 'POST':
        Phone = request.POST.get('PhoneNumber')
        existingMember = Member.objects.filter(PhoneNumber=Phone)
        if existingMember:
            messages.success(request, f"Your Member ID is {existingMember[0].Code}")
            return redirect('/ObtainMemberID') 
        else:
            messages.error(request, "Member with the below data does not exist")  
            return redirect('/ObtainMemberID')
        
    return render(request, 'TAEApp/public/ObtainMemberID.html') 

def ObtainPassword(request):
    if request.method == 'POST':
        MemberID = request.POST.get('MemberID')
        existingMember = Member.objects.filter(Code=MemberID)
        otpText =  OTP()
        
        if existingMember:
            Email = existingMember[0].EmailAddress
            Password = f'{now().month}{now().day}{now().hour}{now().minute}'
            coolCode = Password
            otpText.Code = coolCode
            otpText.isActive = True
            otpText.MemberID = MemberID
            otpText.save()
            text = f'TAE One Time Password is {coolCode}.'
            messages.success(request, f'Your verification code is sent to {Email}' )
            EmailSender(text, Email)
            return redirect('/VerifyCode') 
        else:
            messages.error(request, "Member with the below data does not exist")  
            return redirect('/ObtainPassword')
        
    return render(request, 'TAEApp/public/ObtainPassword.html') 

def ObtainCode(request):
    if request.method == 'POST':
        MemberID = request.POST.get('MemberID')
        existingMember = Member.objects.filter(Code=MemberID)
        otpText =  OTP()
        
        if existingMember:
            Email = existingMember[0].EmailAddress
            Password = f'{now().month}{now().day}{now().hour}{now().minute}'
            coolCode = Password
            otpText.Code = coolCode
            otpText.isActive = True
            otpText.MemberID = MemberID
            otpText.save()
            text = f'TAE One Time Password is {coolCode}.'
            messages.success(request, f'Your verification code is sent to {Email}' )
            EmailSender(text, Email)
            return redirect('/VerifyCodeCommittee') 
        else:
            messages.error(request, "Member with the below data does not exist")  
            return redirect('/ObtainCode')
        
    return render(request, 'TAEApp/public/ObtainPassword.html') 

def VerifyCode(request):
    if request.method == 'POST':
        
        otp = request.POST.get('OTP')
        existingOTP = OTP.objects.filter(Code=otp)
        if existingOTP:
                existingCode = existingOTP[0].Code
                isActive = existingOTP[0].isActive
                memberID = existingOTP[0].MemberID
                # if isActive == True:
                #     messages.error(request, "Verification code already been used.")  
                #     return redirect('/VerifyCode')  
                if existingCode == otp:
                    existingOTP[0].save()
                    request.session['memberID'] = memberID
                    return redirect('/ApplyForElection')  
                else:
                    messages.error(request, "Verification code is not valid")  
                    return redirect('/VerifyCode')             
            
    return render(request, 'TAEApp/public/VerifyCode.html') 

def VerifyCodeCommittee(request):
    if request.method == 'POST':
        
        otp = request.POST.get('OTP')
        existingOTP = OTP.objects.filter(Code=otp)
        if existingOTP:
                existingCode = existingOTP[0].Code
                isActive = existingOTP[0].isActive
                memberID = existingOTP[0].MemberID
                # if isActive == True:
                #     messages.error(request, "Verification code already been used.")  
                #     return redirect('/VerifyCode')  
                if existingCode == otp:
                    existingOTP[0].save()
                    request.session['memberID'] = memberID
                    return redirect('/ApplyForElectionCommittee')  
                else:
                    messages.error(request, "Verification code is not valid")  
                    return redirect('/VerifyCodeCommittee')             
            
    return render(request, 'TAEApp/public/VerifyCode.html') 

def EmailSender(text, Email):
    _Settings = Settings.objects.all()
    if _Settings:

        #The mail addresses and password
        sender_address = _Settings[0].EmailFrom
        sender_pass = _Settings[0].EmailPassword
        receiver_address = Email
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'A test mail sent by TAE' 
        message.attach(MIMEText(text, 'plain'))
        session = smtplib.SMTP(_Settings[0].SMTPHOST, _Settings[0].SMTPPort) 
        session.starttls() #enable security
        session.login(sender_address, sender_pass) 
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')

@login_required    
def index(request):
    return render(request, 'TAEApp/index.html')  

# Registered Members viewn //////////////////////////////////////////////////////////////////////
@login_required    
def MemberView(request):
    MemberList = Member.objects.all()
    page = request.GET.get('page', 1)
    myFilter = MemberFilter(request.GET, queryset=MemberList)
    MemberList = myFilter.qs 

    paginator = Paginator(MemberList, 50)
    try:
        Members = paginator.page(page)
    except PageNotAnInteger:
        Members = paginator.page(1)
    except EmptyPage:
        Members = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="MemberData.csv"'        
        writer = csv.writer(response)
        writer.writerow(['Member Detail'])       
        writer.writerow(['Code',' First Name','Middle Name','Last Name','gender','City','Street','Permit' ,'Emirate' ,'Phone Number','Email Address','Employment Status','Company Name'])
        users = Member.objects.all().values_list('Code','FirstName','MiddleName','LastName','City','Street','Permit' ,'Emirate' ,'PhoneNumber','EmailAddress','EmploymentStatus','CompanyName')
        for user in users:
            writer.writerow(user)
        return response    
    return render(request, 'TAEApp/Members/list.html', {'Members': Members, 'myFilter':myFilter}) 

@login_required    
def createMember(request):
    form = MemberForm(request.POST or None)
    if request.method == 'POST':

        if form.is_valid():
            newform = form.save(commit=False)
            existingMember = Member.objects.filter(PhoneNumber=newform.PhoneNumber)
            if existingMember:
                messages.success(request, 'Phone Number already exist')
                return render(request, 'TAEApp/Members/create.html', {'form': form})
            else:    
                newform.save()
                Number = newform.id + 20
                Code = f"TAE-{Number}"
                newform.Code = Code
                newform.save()
                messages.success(request, 'Successful added')
                return redirect('/createMember')   
        else:
            messages.error(request, 'Form error')
            return render(request, 'TAEApp/Members/create.html', {'form': form})    
    return render(request, 'TAEApp/Members/create.html', {'form': form})

@login_required    
def editMember(request, pk):
    pickMember = Member.objects.get(pk=pk)
    editForm = MemberForm(request.POST or None, request.FILES or None , instance=pickMember )

    if editForm.is_valid():
        newform = editForm.save(commit=False)
        newform.save()
        Number = newform.id + 20
        Code = f"TAE-{Number}"
        newform.Code = Code
        newform.save()
        return redirect('/Member')
    return render(request, 'TAEApp/Members/update.html', {'form': editForm, 'MemberId':pk})

@login_required    
def deleteMember(request, pk):
    pickMember = Member.objects.get(id=pk)
    if request.method == 'POST':
        pickMember.delete()
        return redirect('/Member')
    context = {'item': pickMember}
    return render(request, 'TAEApp/Members/delete.html', context)

def becomeMember (request):
    form = MemberForm(request.POST or None)
    if request.method == 'POST':

        if form.is_valid():
            newform = form.save(commit=False)
            countryCode = newform.PhoneNumber[0 : 4]
            print(countryCode)
            if countryCode != "+971":
                messages.success(request, 'Phone Number must start with +971')
                return render(request, 'TAEApp/public/memberform.html', {'form': form}) 
            existingMember = Member.objects.filter(PhoneNumber=newform.PhoneNumber)
            if existingMember:
                messages.success(request, 'Phone Number already exist')
                return render(request, 'TAEApp/public/memberform.html', {'form': form})
              
            newform.save()
            Number = newform.id + 20
            Code = f"TAE-{Number}"
            newform.Code = Code
            newform.save()
            Password = f'TAE@{now().year}{now().month}{now().day}{now().hour}{now().minute}'
            messages.success(request, f'TAE Credentials, Username is {newform.Code} and Password is {Password}.')
            return redirect('/becomeMember')   
        else:
            messages.error(request, 'Form error')
            return redirect('/becomeMember')  
    return render(request, 'TAEApp/public/memberform.html', {'form': form})

#Gallery view //////////////////////////////////////////////////////////////////////////
@login_required    
def GalleryView(request):
    Galleries = Gallery.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(Galleries, 50)
    try:
        Galleries = paginator.page(page)
    except PageNotAnInteger:
        Galleries = paginator.page(1)
    except EmptyPage:
        Galleries = paginator.page(paginator.num_pages)
    return render(request, 'TAEApp/Galleries/list.html', {'Galleries': Galleries})  

@login_required    
def createGallery(request):
    form = GalleryForm(request.POST or None, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/createGallery')
    return render(request, 'TAEApp/Galleries/create.html', {'form': form})

@login_required    
def editGallery(request, pk):
    pickGallery = Gallery.objects.get(pk=pk)
    editForm = GalleryForm(request.POST or None ,request.FILES or None, instance=pickGallery)

    if editForm.is_valid():
        editForm.save()
        return redirect('/Gallery')
    return render(request, 'TAEApp/Galleries/update.html', {'form': editForm})


@login_required    
def deleteGallery(request, pk):
    pickGallery = Gallery.objects.get(pk=pk)
    if request.method == 'POST':
        pickGallery.delete()
        return redirect('/Gallery')
    context = {'item': pickGallery} 
    return render(request, 'TAEApp/Galleries/delete.html', context)


#News view //////////////////////////////////////////////////////////////////////////
@login_required    
def NewsView(request):
    _News = News.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(_News, 50)
    try:
        _News = paginator.page(page)
    except PageNotAnInteger:
        _News = paginator.page(1)
    except EmptyPage:
        _News = paginator.page(paginator.num_pages)
    return render(request, 'TAEApp/News/list.html', {'TeaNews': _News})  

@login_required    
def createNews(request):
    form = NewsForm(request.POST or None, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "News created")  
            return redirect('/createNews')
        else:
            messages.error(request, "Form Error")  
    return render(request, 'TAEApp/News/create.html', {'form': form})

@login_required    
def editNews(request, pk):
    pickNews = News.objects.get(pk=pk)
    editForm = NewsForm(request.POST or None,request.FILES or None, instance=pickNews)

    if editForm.is_valid():
        editForm.save()
        return redirect('/News')
    return render(request, 'TAEApp/News/update.html', {'form': editForm, 'NewsId':pk})


@login_required    
def deleteNews(request, pk):
    pickNews = News.objects.get(pk=pk)
    if request.method == 'POST':
        pickNews.delete()
        return redirect('/News')
    context = {'item': pickNews} 
    return render(request, 'TAEApp/News/delete.html', context)


#Complain1 view //////////////////////////////////////////////////////////////////////////
@login_required    
def Complain1View(request):
    _Complain1 = Complain1.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(_Complain1, 50)
    try:
        _Complain1 = paginator.page(page)
    except PageNotAnInteger:
        _Complain1 = paginator.page(1)
    except EmptyPage:
        _Complain1 = paginator.page(paginator.num_pages)
    return render(request, 'TAEApp/Complains/Complain1/list.html', {'TeaComplain1': _Complain1})  

@login_required    
def createComplain1(request):
    form = Complain1Form(request.POST or None, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Complain created")  
            return redirect('/createComplain1')
        else:
            messages.error(request, "Form Error")  
    return render(request, 'TAEApp/Complains/Complain1/create.html', {'form': form})

@login_required    
def editComplain1(request, pk):
    pickComplain1 = Complain1.objects.get(pk=pk)
    editForm = Complain1Form(request.POST or None,request.FILES or None, instance=pickComplain1)

    if editForm.is_valid():
        editForm.save()
        return redirect('/Complain1')
    return render(request, 'TAEApp/Complains/Complain1/update.html', {'form': editForm, 'Complain1Id':pk})


@login_required    
def deleteComplain1(request, pk):
    pickComplain1 = Complain1.objects.get(pk=pk)
    if request.method == 'POST':
        pickComplain1.delete()
        return redirect('/Complain1')
    context = {'item': pickComplain1} 
    return render(request, 'TAEApp/Complains/Complain1/delete.html', context)


#Complain2 view //////////////////////////////////////////////////////////////////////////
@login_required    
def Complain2View(request):
    _Complain2 = Complain2.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(_Complain2, 50)
    try:
        _Complain2 = paginator.page(page)
    except PageNotAnInteger:
        _Complain2 = paginator.page(1)
    except EmptyPage:
        _Complain2 = paginator.page(paginator.num_pages)
    return render(request, 'TAEApp/Complains/Complain2/list.html', {'TeaComplain2': _Complain2})  

@login_required    
def createComplain2(request):
    form = Complain2Form(request.POST or None, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            newform = form.save(commit=False)
            existingMember = Member.objects.filter(Code=newform.TAENumber)
            if existingMember:
                newform.save()
                messages.success(request, "Complain created") 
            else:
                form = newform
                messages.error(request, "Member Code does not exist")  
            return redirect('/createComplain2')
        else:
            messages.error(request, "Form Error")  
    return render(request, 'TAEApp/Complains/Complain2/create.html', {'form': form})

@login_required    
def editComplain2(request, pk):
    pickComplain2 = Complain2.objects.get(pk=pk)
    editForm = Complain2Form(request.POST or None,request.FILES or None, instance=pickComplain2)

    if editForm.is_valid():
            newform = editForm.save(commit=False)
            existingMember = Member.objects.filter(Code=newform.TAENumber)
            if existingMember :
                newform.save()
                messages.success(request, "Complain created") 
                return redirect('/Complain2')
            else:
                form = newform
                messages.error(request, "Member Code does not exist")  
    
    return render(request, 'TAEApp/Complains/Complain2/update.html', {'form': editForm, 'Complain2Id':pk})


@login_required    
def deleteComplain2(request, pk):
    pickComplain2 = Complain2.objects.get(pk=pk)
    if request.method == 'POST':
        pickComplain2.delete()
        return redirect('/Complain2')
    context = {'item': pickComplain2} 
    return render(request, 'TAEApp/Complains/Complain2/delete.html', context)

def ComplainTwo(request):
    form = Complain2Form(request.POST or None, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            newform = form.save(commit=False)
            existingMember = Member.objects.filter(Code=newform.TAENumber)
            if existingMember:
                newform.save()
                messages.success(request, "Complain submitted") 
                return redirect('/ComplainTwo')
            else:
                messages.error(request, "Member Code does not exist")
                return render(request, 'TAEApp/public/ComplainTwo.html', {'form': form})  
            
        else:
            messages.error(request, "Form Error") 
            return render(request, 'TAEApp/public/ComplainTwo.html', {'form': form}) 
    return render(request, 'TAEApp/public/ComplainTwo.html', {'form': form})

def ComplainOne(request):
    form = Complain1Form(request.POST or None, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Complain submitted")  
            return render(request, 'TAEApp/public/ComplainOne.html', {'form': form}) 
        else:
            messages.error(request, "Form Error") 
            return render(request, 'TAEApp/public/ComplainOne.html', {'form': form})  
    return render(request, 'TAEApp/public/ComplainOne.html', {'form': form}) 

#ElectionApplicant view //////////////////////////////////////////////////////////////////////////
@login_required    
def ElectionApplicantView(request):
    _ElectionApplicant = ElectionApplicant.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(_ElectionApplicant, 50)
    try:
        _ElectionApplicant = paginator.page(page)
    except PageNotAnInteger:
        _ElectionApplicant = paginator.page(1)
    except EmptyPage:
        _ElectionApplicant = paginator.page(paginator.num_pages)
    return render(request, 'TAEApp/ElectionApplicant/list.html', {'TeaElectionApplicant': _ElectionApplicant})  

@login_required    
def createElectionApplicant(request):
    form = ElectionApplicantForm(request.POST or None, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            newform = form.save(commit=False)
            existingMember = Member.objects.filter(Code=newform.TAENumber)
            if existingMember:
                newform.save()
                messages.success(request, "Complain created") 
            else:
                form = newform
                messages.error(request, "Member Code does not exist")  
            return redirect('/createElectionApplicant')
        else:
            messages.error(request, "Form Error")  
    return render(request, 'TAEApp/ElectionApplicant/create.html', {'form': form})

@login_required    
def editElectionApplicant(request, pk):
    pickElectionApplicant = ElectionApplicant.objects.get(pk=pk)
    editForm = ElectionApplicantForm(request.POST or None,request.FILES or None, instance=pickElectionApplicant)

    if editForm.is_valid():
            newform = editForm.save(commit=False)
            existingMember = Member.objects.filter(Code=newform.Code)
            if existingMember :
                newform.save()
                messages.success(request, "Complain created") 
                return redirect('/ElectionApplicant')
            else:
                form = newform
                messages.error(request, "Member Code does not exist")  
    
    return render(request, 'TAEApp/ElectionApplicant/update.html', {'form': editForm, 'Id':pk, 'ElectionApplicantId':pk})


@login_required    
def deleteElectionApplicant(request, pk):
    pickElectionApplicant = ElectionApplicant.objects.get(pk=pk)
    if request.method == 'POST':
        pickElectionApplicant.delete()
        return redirect('/ElectionApplicant')
    context = {'item': pickElectionApplicant} 
    return render(request, 'TAEApp/ElectionApplicant/delete.html', context)   

def PublicApplicant(request):
    Applicant = ElectionApplicant()
    if 'memberID' in request.session:
        MemberID = request.session['memberID']
        member = Member.objects.filter(Code = MemberID)
        if member:
            Applicant.FirstName = member[0].FirstName
            Applicant.MiddleName = member[0].MiddleName
            Applicant.LastName = member[0].LastName
            Applicant.Emirate = member[0].Emirate
            #Applicant.EmploymentStatus = member[0].EmploymentStatus
            Applicant.Code = MemberID
    Applicantform = ElectionApplicantForm(instance=Applicant )
    form = ElectionApplicantForm(request.POST or None, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            newform = form.save(commit=False)
            existingMember = Member.objects.filter(Code=newform.Code)
            if existingMember:
                existingMemberApplication = ElectionApplicant.objects.filter(Code=newform.Code)
                if existingMemberApplication:
                    messages.error(request, "You have already applied the position.")  
                    return render(request, 'TAEApp/public/ElectionApplication.html', {'form': Applicantform})
                newform.save()
                messages.success(request, "Application submitted") 
                return redirect("/ObtainPassword")
            else:
                form = newform
                messages.error(request, "Member Code does not exist")  
            return render(request, 'TAEApp/public/ElectionApplication.html', {'form': Applicantform})
        else:
            messages.error(request, "Form Error")
            return render(request, 'TAEApp/public/ElectionApplication.html', {'form': Applicantform})  
    return render(request, 'TAEApp/public/ElectionApplication.html', {'form': Applicantform})


    #FrontPage view //////////////////////////////////////////////////////////////////////////
@login_required    
def FrontPageView(request):
    _FrontPage = FrontPage.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(_FrontPage, 50)
    try:
        _FrontPage = paginator.page(page)
    except PageNotAnInteger:
        _FrontPage = paginator.page(1)
    except EmptyPage:
        _FrontPage = paginator.page(paginator.num_pages)
    return render(request, 'TAEApp/CMS/FrontPage/list.html', {'TeaFrontPage': _FrontPage})  

@login_required    
def createFrontPage(request):
    form = FrontPageForm(request.POST or None, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Content created")  
            return redirect('/createFrontPage')
        else:
            messages.error(request, "Form Error")  
    return render(request, 'TAEApp/CMS/FrontPage/create.html', {'form': form})

@login_required    
def editFrontPage(request, pk):
    pickFrontPage = FrontPage.objects.get(pk=pk)
    editForm = FrontPageForm(request.POST or None,request.FILES or None, instance=pickFrontPage)

    if editForm.is_valid():
        editForm.save()
        return redirect('/FrontPage')
    return render(request, 'TAEApp/CMS/FrontPage/update.html', {'form': editForm, 'Id':pk})


@login_required    
def deleteFrontPage(request, pk):
    pickFrontPage = FrontPage.objects.get(pk=pk)
    if request.method == 'POST':
        pickFrontPage.delete()
        return redirect('/FrontPage')
    context = {'item': pickFrontPage} 
    return render(request, 'TAEApp/CMS/FrontPage/delete.html', context)
    

 #Content view //////////////////////////////////////////////////////////////////////////
@login_required    
def ContentView(request):
    _Content = Content.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(_Content, 50)
    try:
        _Content = paginator.page(page)
    except PageNotAnInteger:
        _Content = paginator.page(1)
    except EmptyPage:
        _Content = paginator.page(paginator.num_pages)
    return render(request, 'TAEApp/CMS/Content/list.html', {'TeaContent': _Content})  

@login_required    
def createContent(request):
    form = ContentForm(request.POST or None, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Content created")  
            return redirect('/createContent')
        else:
            messages.error(request, "Form Error")  
    return render(request, 'TAEApp/CMS/Content/create.html', {'form': form})

@login_required    
def editContent(request, pk):
    pickContent = Content.objects.get(pk=pk)
    editForm = ContentForm(request.POST or None,request.FILES or None, instance=pickContent)

    if editForm.is_valid():
        editForm.save()
        return redirect('/Content')
    return render(request, 'TAEApp/CMS/Content/update.html', {'form': editForm, 'Id':pk})


@login_required    
def deleteContent(request, pk):
    pickContent = Content.objects.get(pk=pk)
    if request.method == 'POST':
        pickContent.delete()
        return redirect('/Content')
    context = {'item': pickContent} 
    return render(request, 'TAEApp/CMS/Content/delete.html', context)
    
#ElectionCommitteeApplicant view //////////////////////////////////////////////////////////////////////////
@login_required    
def ElectionCommitteeApplicantView(request):
    _ElectionCommitteeApplicant = ElectionCommitteeApplicant.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(_ElectionCommitteeApplicant, 50)
    try:
        _ElectionCommitteeApplicant = paginator.page(page)
    except PageNotAnInteger:
        _ElectionCommitteeApplicant = paginator.page(1)
    except EmptyPage:
        _ElectionCommitteeApplicant = paginator.page(paginator.num_pages)
    return render(request, 'TAEApp/ElectionCommitteeApplicant/list.html', {'TeaElectionCommitteeApplicant': _ElectionCommitteeApplicant})  

@login_required    
def createElectionCommitteeApplicant(request):
    form = ElectionCommitteeApplicantForm(request.POST or None, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            newform = form.save(commit=False)
            existingMember = Member.objects.filter(Code=newform.TAENumber)
            if existingMember:
                newform.save()
                messages.success(request, "Complain created") 
            else:
                form = newform
                messages.error(request, "Member Code does not exist")  
            return redirect('/createElectionCommitteeApplicant')
        else:
            messages.error(request, "Form Error")  
    return render(request, 'TAEApp/ElectionCommitteeApplicant/create.html', {'form': form})

@login_required    
def editElectionCommitteeApplicant(request, pk):
    pickElectionCommitteeApplicant = ElectionCommitteeApplicant.objects.get(pk=pk)
    editForm = ElectionCommitteeApplicantForm(request.POST or None,request.FILES or None, instance=pickElectionCommitteeApplicant)

    if editForm.is_valid():
            newform = editForm.save(commit=False)
            existingMember = Member.objects.filter(Code=newform.Code)
            if existingMember :
                newform.save()
                messages.success(request, "Complain created") 
                return redirect('/ElectionCommitteeApplicant')
            else:
                form = newform
                messages.error(request, "Member Code does not exist")  
    
    return render(request, 'TAEApp/ElectionCommitteeApplicant/update.html', {'form': editForm, 'Id':pk, 'ElectionCommitteeApplicantId':pk})


@login_required    
def deleteElectionCommitteeApplicant(request, pk):
    pickElectionCommitteeApplicant = ElectionCommitteeApplicant.objects.get(pk=pk)
    if request.method == 'POST':
        pickElectionCommitteeApplicant.delete()
        return redirect('/ElectionCommitteeApplicant')
    context = {'item': pickElectionCommitteeApplicant} 
    return render(request, 'TAEApp/ElectionCommitteeApplicant/delete.html', context)   

def PublicCommitteApplicant(request):
    Applicant = ElectionCommitteeApplicant()
    if 'memberID' in request.session:
        MemberID = request.session['memberID']
        member = Member.objects.filter(Code = MemberID)
        if member:
            Applicant.FirstName = member[0].FirstName
            Applicant.MiddleName = member[0].MiddleName
            Applicant.LastName = member[0].LastName
            Applicant.Emirate = member[0].Emirate
            #Applicant.EmploymentStatus = member[0].EmploymentStatus
            Applicant.Code = MemberID
    Applicantform = ElectionCommitteeApplicantForm(instance=Applicant )
    form = ElectionCommitteeApplicantForm(request.POST or None, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            newform = form.save(commit=False)
            existingMember = Member.objects.filter(Code=newform.Code)
            if existingMember:
                existingMemberApplication = ElectionCommitteeApplicant.objects.filter(Code=newform.Code)
                if existingMemberApplication:
                    messages.error(request, "You have already applied the position.")  
                    return render(request, 'TAEApp/public/ElectionCommitteApplication.html', {'form': Applicantform})
                newform.save()
                messages.success(request, "Application submitted") 
                return redirect("/ObtainCode")
            else:
                form = newform
                messages.error(request, "Member Code does not exist")  
            return render(request, 'TAEApp/public/ElectionCommitteApplication.html', {'form': Applicantform})
        else:
            messages.error(request, "Form Error")
            return render(request, 'TAEApp/public/ElectionCommitteApplication.html', {'form': Applicantform})  
    return render(request, 'TAEApp/public/ElectionCommitteApplication.html', {'form': Applicantform})

#Settings view //////////////////////////////////////////////////////////////////////////
@login_required    
def SettingsView(request):
    _Settings = Settings.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(_Settings, 50)
    try:
        _Settings = paginator.page(page)
    except PageNotAnInteger:
        _Settings = paginator.page(1)
    except EmptyPage:
        _Settings = paginator.page(paginator.num_pages)
    return render(request, 'TAEApp/Settings/list.html', {'TeaSettings': _Settings})  

@login_required    
def createSettings(request):
    form = SettingsForm(request.POST or None, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Settings created")  
            return redirect('/createSettings')
        else:
            messages.error(request, "Form Error")  
    return render(request, 'TAEApp/Settings/create.html', {'form': form})

@login_required    
def editSettings(request, pk):
    pickSettings = Settings.objects.get(pk=pk)
    editForm = SettingsForm(request.POST or None,request.FILES or None, instance=pickSettings)

    if editForm.is_valid():
        editForm.save()
        return redirect('/Settings')
    return render(request, 'TAEApp/Settings/update.html', {'form': editForm, 'SettingsId':pk})


@login_required    
def deleteSettings(request, pk):
    pickSettings = Settings.objects.get(pk=pk)
    if request.method == 'POST':
        pickSettings.delete()
        return redirect('/Settings')
    context = {'item': pickSettings} 
    return render(request, 'TAEApp/Settings/delete.html', context)
