from typing import Sequence
from django.db import models
from django.forms import CharField
from h11 import Data

# Create your models here.   


Permits =(("Residence", "Residence"),("Visit", "Visit"))
Emirates =(("Abu Dhabi", "Abu Dhabi"),("Dubai","Dubai"),("Sharjah ","Sharjah "),("Ajman","Ajman"),("Umm Al Quwain ","Umm Al Quwain "),("Ras Al Khaimah","Ras Al Khaimah"),("Fujairah","Fujairah"))
EmploymentStatuses =(("Full time","Full time"), ("Part time ","Part time "),("Not applicable","Not applicable"), ("Job Seeker","Job Seeker"), ("Own a business","Own a business"), ("Self-employer","Self-employer" ))
genders =(("Male", "Male"),("Female", "Female"),)
VisaTypes = (("Golden visa", "Golden visa"),("Residence visa","Residence visa"),("Visit visa ","Visit visa "),("Transit visa","Transit visa"))
Educations =(("Secondary school", "Secondary school"),("High school","High school"),("Certificate ","Certificate "),("Diploma","Diploma"),("Bachelor","Bachelor"),("Masters","Masters"),("PhD","PhD"))

class Member(models.Model):
    Code = models.CharField(max_length=200, blank=True)
    FirstName =  models.CharField(max_length=200, verbose_name="First Name")
    MiddleName =  models.CharField(max_length=200, verbose_name="Middle Name")
    LastName =  models.CharField(max_length=200, verbose_name="Last Name")
    # Photo  = models.ImageField()
    # PhotoURL = models.URLField(max_length=500, blank=True)
    # Gender = models.CharField(max_length=500,choices=genders)
    Nationality =  models.CharField(max_length=200, verbose_name="Nationality")
    City =  models.CharField(max_length=200)
    Street =  models.CharField(max_length=200, verbose_name="Street")
    Permit =  models.CharField(max_length=200, choices=Permits, verbose_name="Home Address")
    Emirate =  models.CharField(max_length=200, choices=Emirates, verbose_name="Emirate")
    PhoneNumber =  models.CharField(max_length=200, verbose_name="Phone Number")
    EmailAddress =  models.EmailField(max_length=200, verbose_name="Email")
    EmploymentStatus =  models.CharField(max_length=200, choices=EmploymentStatuses, verbose_name="Religion")
    CompanyName =  models.CharField(max_length=200, verbose_name="Company Name")
    DoYouKnowAboutTAE =  models.BooleanField(default=False, verbose_name="Do You Know About TAE")
    Advice = models.TextField(max_length=200,blank=True, default='')
    def __str__(self):
        Fullname = f'{self.FirstName} {self.MiddleName} {self.LastName}'
        return Fullname

class Gallery(models.Model):
     Photo  = models.ImageField(upload_to='images/Events/Gallery/')

class Category(models.Model):
       Name =  models.CharField(max_length=50) 

class Event(models.Model):
     Category = models.ForeignKey(Category, verbose_name="Category", on_delete=models.CASCADE)
     Gallery = models.ManyToManyField(Gallery)
     Photo  = models.ImageField(upload_to='images/Events/')
     Title =  models.CharField(max_length=50)
     Description1 =  models.TextField(max_length=200)
     Description2 =  models.TextField(max_length=200, blank=True)
     PublishDate = models.DateTimeField(auto_now_add=True, blank=True)
     def __str__(self):
        return self.Title

class News(models.Model):
     Photo  = models.ImageField(upload_to='images')
     Title =  models.CharField(max_length=50)
     Description1 =  models.TextField(max_length=200)
     Description2 =  models.TextField(max_length=200, blank=True)
     PublishDate = models.DateTimeField(auto_now_add=True, blank=True)
     def __str__(self):
        return self.Title

Services =(("Kazi UAE", "Kazi UAE"),("Kununua Biashara", "Kununua Biashara"),("Matibabu", "Matibabu"),("Masomo", "Masomo"),("Mengine", "Mengine"),)
class Complain1(models.Model):
     FullName =  models.CharField(max_length=50)
     PhoneUAE =  models.CharField(max_length=50, blank=True)
     PhoneTZ =  models.CharField(max_length=50, blank=True)
     Address =  models.CharField(max_length=50)
     AgentName =  models.CharField(max_length=50)
     AgentPhoneTZ =  models.CharField(max_length=50, blank=True)
     AgentPhoneUAE =  models.CharField(max_length=50, blank=True)
     ServiceType =  models.CharField(choices=Services, max_length=50,)
     VisaType =  models.CharField(max_length=50, choices=VisaTypes,)
     VisaStatus =  models.CharField(max_length=50)
     AmountPaidTZ =  models.CharField(max_length=50, blank=True)
     AmountPaidUAE =  models.CharField(max_length=50, blank=True)
     Description =  models.TextField(max_length=100)
     Date = models.DateTimeField(auto_now_add=True, blank=True)
     def __str__(self):
        return self.FullName        

class Complain2(models.Model):
     TAENumber =  models.CharField(max_length=50)
     FullName =  models.CharField(max_length=50)
     Phone =  models.CharField(max_length=50)
     CompanyOrSponsor =  models.CharField(max_length=50)
     Position =  models.CharField(max_length=50)
     JobYears =  models.IntegerField()
     Complain =  models.TextField(max_length=100)
     TakenSteps =  models.TextField(max_length=100)
     Recommendation =  models.TextField(max_length=100)
     Date = models.DateTimeField(auto_now_add=True, blank=True)
     def __str__(self):
        return self.FullName 


class Feedback(models.Model):
    IsMember=models.BooleanField(default=False, verbose_name="Are you a TAE member")
    Code = models.CharField(max_length=200, blank=True)
    FullName =  models.CharField(max_length=200, verbose_name="Full Name")
    Gender = models.CharField(max_length=500,choices=genders)
    Nationality =  models.CharField(max_length=200, verbose_name="Nationality")
    Emirate =  models.CharField(max_length=200, choices=Emirates, verbose_name="Emirate")
    Feedback =  models.TextField(max_length=100, verbose_name="Your Feedback")
    ShareWithOthers=models.BooleanField(default=False, verbose_name="Do you want to share your feedback with others yes/no")
    def __str__(self):
        return self.FullName

Positions =(("Chairman of the association","Chairman of the association"),("Vice Chairman of the Association","Vice Chairman of the Association"),("Secretary General","Secretary General"),("Deputy Secretary General","Deputy Secretary General"),("Treasurer","Treasurer"),("Assistant Treasurer","Assistant Treasurer"),("Chairman of the Chairman of Cultural and Social Welfare Committee","Chairman of the Chairman of Cultural and Social Welfare Committee"),("Chairman of the Chairman of Budget and Finance Committee","Chairman of the Chairman of Budget and Finance Committee"),("Chairman of the Chairman of knowledge and Publicity Committee","Chairman of the Chairman of knowledge and Publicity Committee"),("Chairman of the Chairman of Homeland investment committee","Chairman of the Chairman of Homeland investment committee"),("Committee member of Cultural and Social Welfare Committee","Committee member of Cultural and Social Welfare Committee"),("Committee member of Budget and Finance Committee","Committee member of Budget and Finance Committee"),("Committee member of knowledge and Publicity Committee","Committee member of knowledge and Publicity Committee"),("Committee member of Homeland investment committee","Committee member of Homeland investment committee"),)
class ElectionApplicant(models.Model):
    Code = models.CharField(max_length=200, verbose_name="Membership Code" )
    FirstName =  models.CharField(max_length=200, verbose_name="First Name")
    MiddleName =  models.CharField(max_length=200, verbose_name="Middle Name")
    LastName =  models.CharField(max_length=200, verbose_name="Last Name")
    EmirateID  = models.ImageField(upload_to='images', verbose_name="Attach Emirate ID")
    VisaType =  models.CharField(max_length=200, choices=VisaTypes, verbose_name="Visa Type")
    Education =  models.CharField(max_length=200, choices=Educations, verbose_name="Education")
    Emirate =  models.CharField(max_length=200, choices=Emirates, verbose_name="Emirate")
    Position = models.CharField(max_length=100, choices=Positions, verbose_name="Position" )
    EmploymentStatus =  models.CharField(max_length=200, choices=EmploymentStatuses, verbose_name="Religion")
    def __str__(self):
        Fullname = f'{self.FirstName} {self.MiddleName} {self.LastName}'
        return Fullname

class FrontPage(models.Model):
     Photo  = models.ImageField(upload_to='images')
     Title =  models.CharField(max_length=50)
     Description1 =  models.TextField(max_length=200)
     PublishDate = models.DateTimeField(auto_now_add=True, blank=True)
     def __str__(self):
        return self.Title   

class Content(models.Model):
     Title =  models.CharField(max_length=100)
     Description1 =  models.TextField(max_length=1000)
#      Sequence = models.IntegerField()
     def __str__(self):
        return self.Title 

class ForgotID(models.Model):
        Phone =  models.CharField(max_length=15)
        FirstName =  models.CharField(max_length=50)
        LastName =  models.CharField(max_length=50)
        def __str__(self):
           return self.Phone   

class Article(models.Model):
     Photo  = models.ImageField(upload_to='images')
     Title =  models.CharField(max_length=50)
     Description =  models.TextField(max_length=200)
     PublishDate = models.DateTimeField(auto_now_add=True, blank=True)
     EndDate = models.DateTimeField(auto_now_add=True, blank=True)
     isActive = models.BooleanField(default=False)
     def __str__(self):
        return self.Title                              