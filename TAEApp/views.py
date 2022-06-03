from distutils.log import error
from email import message
import uuid
from django.http import HttpResponse
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
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
 
import csv
# Create your views here.
# Create your views here.
def home(request):
    Galleries = Gallery.objects.all()
    TaeNews = News.objects.all()
    SampleNews = TaeNews[0:4]
    images = Galleries[1:8]
    return render(request, 'home.html',{'Galleries':images, 'News':SampleNews})    

def publicGallery(request):
    Galleries = Gallery.objects.all()
    
    return render(request, 'TAEApp/public/publicGallery.html',{'Galleries':Galleries})  

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
            newform.save()
            Number = newform.id + 20
            Code = f"TAE-{Number}"
            newform.Code = Code
            newform.save()
            messages.success(request, 'Successful added')
            return redirect('/createMember')   
        else:
            messages.error(request, 'Form error')
            return redirect('/createMember')    
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
            newform.save()
            Number = newform.id + 20
            Code = f"TAE-{Number}"
            newform.Code = Code
            newform.save()
            Password = f'TAE@{now().year}{now().month}{now().day}{now().hour}{now().minute}'
            messages.success(request, f'TAE Credentials, Username is {newform.Code} and Password is {Password}, Also we sent your Credentials to your email.')
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
            else:
                form = newform
                messages.error(request, "Member Code does not exist")  
            return redirect('/ComplainTwo')
        else:
            messages.error(request, "Form Error")  
    return render(request, 'TAEApp/public/ComplainTwo.html', {'form': form})

def ComplainOne(request):
    form = Complain1Form(request.POST or None, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Complain submitted")  
            return redirect('/ComplainTwo')
        else:
            messages.error(request, "Form Error")  
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
            existingMember = Member.objects.filter(Code=newform.TAENumber)
            if existingMember :
                newform.save()
                messages.success(request, "Complain created") 
                return redirect('/ElectionApplicant')
            else:
                form = newform
                messages.error(request, "Member Code does not exist")  
    
    return render(request, 'TAEApp/ElectionApplicant/update.html', {'form': editForm, 'ElectionApplicantId':pk})


@login_required    
def deleteElectionApplicant(request, pk):
    pickElectionApplicant = ElectionApplicant.objects.get(pk=pk)
    if request.method == 'POST':
        pickElectionApplicant.delete()
        return redirect('/ElectionApplicant')
    context = {'item': pickElectionApplicant} 
    return render(request, 'TAEApp/ElectionApplicant/delete.html', context)   

def PublicApplicant(request):
    form = ElectionApplicantForm(request.POST or None, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            newform = form.save(commit=False)
            existingMember = Member.objects.filter(Code=newform.TAENumber)
            if existingMember:
                newform.save()
                messages.success(request, "Application submitted") 
            else:
                form = newform
                messages.error(request, "Member Code does not exist")  
            return redirect('/ApplyForElection')
        else:
            messages.error(request, "Form Error")  
    return render(request, 'TAEApp/public/ElectionApplication.html', {'form': form})    