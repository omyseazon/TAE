import django_filters
from django_filters import DateFilter
from .models import *

class MemberFilter(django_filters.FilterSet):
    class Meta:
        #minimum of two attr
        model = Member
        #2) all & exclude(override all)
        fields = ('Code','FirstName','MiddleName', 'LastName')


class NewsFilter(django_filters.FilterSet):
    class Meta:
        #minimum of two attr
        model = News
        #2) all & exclude(override all)
        fields = ('Title',)

class Complain1Filter(django_filters.FilterSet):
    class Meta:
        #minimum of two attr
        model = Complain1
        #2) all & exclude(override all)
        fields = ('FullName',)

class Complain2Filter(django_filters.FilterSet):
    class Meta:
        #minimum of two attr
        model = Complain2
        #2) all & exclude(override all)
        fields = ('FullName',)                  

class ElectionApplicantFilter(django_filters.FilterSet):
    class Meta:
        #minimum of two attr
        model = ElectionApplicant
        #2) all & exclude(override all)
        fields = ('Code',)        