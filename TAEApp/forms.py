# forms.py
from random import sample
from django import forms
from .models import *
from .widget import DatePickerInput, TimePickerInput, DateTimePickerInput


class MemberForm(forms.ModelForm):
	class Meta:
		model = Member
		fields = '__all__'
		
class GalleryForm(forms.ModelForm):
	class Meta:
		model = Gallery
		fields = '__all__'
# class StudentAdmissionForm(forms.ModelForm):
# 	class Meta:
# 		model = StudentAdmission
# 		fields = '__all__'
# 		exclude = ('AdmissionNumber','PaymentStatus','BirthCertificateUrl','ResultCertificateUrl','PhotoURL','AdmissionDate','FormStatus','RegistrationStatus')
# 		widgets = {
#             'DateOfBirth' : DatePickerInput(),
#         }

class NewsForm(forms.ModelForm):
	class Meta:
		model = News
		fields = '__all__'

class Complain1Form(forms.ModelForm):
	class Meta:
		model = Complain1
		fields = '__all__'

class Complain2Form(forms.ModelForm):
	class Meta:
		model = Complain2
		fields = '__all__'

class ElectionApplicantForm(forms.ModelForm):
	class Meta:
		model = ElectionApplicant
		fields = '__all__'		

class FrontPageForm(forms.ModelForm):
	class Meta:
		model = FrontPage
		fields = '__all__'		

class ContentForm(forms.ModelForm):
	class Meta:
		model = Content
		fields = '__all__'			