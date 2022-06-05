from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include

urlpatterns = [
      
      
       #Member urls
      path('Member', views.MemberView, name = 'Member'),
      path('createMember', views.createMember, name = 'createMember'),
      path('updateMember/<int:pk>', views.editMember, name = 'updateMember'),
      path('deleteMember/<int:pk>', views.deleteMember, name='deleteMember'),

        #Gallery urls
      path('Gallery', views.GalleryView, name = 'Gallery'),
      path('createGallery', views.createGallery, name = 'createGallery'),
      path('updateGallery/<int:pk>', views.editGallery, name = 'updateGallery'),
      path('deleteGallery/<int:pk>', views.deleteGallery, name='deleteGallery'),

        #News urls
      path('News', views.NewsView, name = 'News'),
      path('createNews', views.createNews, name = 'createNews'),
      path('updateNews/<int:pk>', views.editNews, name = 'updateNews'),
      path('deleteNews/<int:pk>', views.deleteNews, name='deleteNews'),

        #Complain1 urls
      path('Complain1', views.Complain1View, name = 'Complain1'),
      path('createComplain1', views.createComplain1, name = 'createComplain1'),
      path('updateComplain1/<int:pk>', views.editComplain1, name = 'updateComplain1'),
      path('deleteComplain1/<int:pk>', views.deleteComplain1, name='deleteComplain1'),

      #Complain2 urls
      path('Complain2', views.Complain2View, name = 'Complain2'),
      path('createComplain2', views.createComplain2, name = 'createComplain2'),
      path('updateComplain2/<int:pk>', views.editComplain2, name = 'updateComplain2'),
      path('deleteComplain2/<int:pk>', views.deleteComplain2, name='deleteComplain2'),

       #ElectionApplicant urls
      path('ElectionApplicant', views.ElectionApplicantView, name = 'ElectionApplicant'),
      path('createElectionApplicant', views.createElectionApplicant, name = 'createElectionApplicant'),
      path('updateElectionApplicant/<int:pk>', views.editElectionApplicant, name = 'updateElectionApplicant'),
      path('deleteElectionApplicant/<int:pk>', views.deleteElectionApplicant, name='deleteElectionApplicant'),

       #public urls
      path('becomeMember', views.becomeMember, name='becomeMember'),
      path('publicGallery', views.publicGallery, name='publicGallery'),
      path('ComplainOne', views.ComplainOne, name='ComplainOne'),
      path('ComplainTwo', views.ComplainTwo, name='ComplainTwo'),
      path('ApplyForElection', views.PublicApplicant, name='ApplyForElection'),

      #FrontPage urls
      path('FrontPage', views.FrontPageView, name = 'FrontPage'),
      path('createFrontPage', views.createFrontPage, name = 'createFrontPage'),
      path('updateFrontPage/<int:pk>', views.editFrontPage, name = 'updateFrontPage'),
      path('deleteFrontPage/<int:pk>', views.deleteFrontPage, name='deleteFrontPage'),
      
       #Content urls
      path('Content', views.ContentView, name = 'Content'),
      path('createContent', views.createContent, name = 'createContent'),
      path('updateContent/<int:pk>', views.editContent, name = 'updateContent'),
      path('deleteContent/<int:pk>', views.deleteContent, name='deleteContent'),

      #basic urls
      path('dashboard', views.index, name='index'),
      path('', views.home, name='home'),
      path('accounts/', include('django.contrib.auth.urls')),
    # path('update/<str:pk>/', views.updatingTask, name='update'),
    # path('delete/<str:pk>/', views.deleteTask, name='delete'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)