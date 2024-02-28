"""
URL configuration for school project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from login import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.login, name='login'),
    path('admin/', admin.site.urls),
    path('home/', views.index, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('login/index/', views.index, name='index'),
    path('det/', views.userdetails, name='userdetails'),
    path('adminpage/', views.admin_page, name='adminpage'),
    path('add_school/', views.add_school, name='add_school'),
    path('add_school_save/', views.add_school_save, name='add_school_save'),
    path('add_student/', views.add_student, name='add_student'),
    path('add_student_save/', views.add_student_save, name='add_student_save'),
    path('add_personnel/', views.add_personnel, name='add_personnel'),
    path('add_personnel_save/', views.add_personnel_save, name='add_personnel_save'),
    path('add_classe/', views.add_classe, name='add_classe'),
    path('add_classe_save/', views.add_classe_save, name='add_classe_save'),
    path('add_matiere/', views.add_matiere, name='add_matiere'),
    path('add_matiere_save/', views.add_matiere_save, name='add_matiere_save'),
    path('manage_personnel/', views.manage_personnel, name='manage_personnel'),
    path('manage_student/', views.manage_student, name='manage_student'),
    path('manage_classe/', views.manage_classe, name='manage_classe'),
    path('etudiants/<int:id>/', views.list_etudiant_par_classe, name='list_etudiant_par_classe'),
    path('edit_student/<str:student_id>/', views.edit_student, name='edit_student'),
    path('edit_student_save/', views.edit_student_save, name='edit_student_save'),
    path('edit_personnel/<str:pers_id>/', views.edit_personnel, name='edit_personnel'),
    path('edit_personnel_save/', views.edit_personnel_save, name='edit_personnel_save'),
    path('edit_matiere/<str:mat_id>/', views.edit_matiere, name='edit_matiere'),
    path('edit_matiere_save/', views.edit_matiere_save, name='edit_matiere_save'),
    path('add_result/', views.personnel_add_result, name='add_result'),
    path('save_result/', views.save_result, name='save_result'),
    path('supprimer_personnel/<str:pers_id>/', views.delete_personnel, name='delete_personnel'),
    path('manage_matiere/', views.manage_matiere, name='manage_matiere'),
    path('delete_matiere/<str:mat_id>/', views.delete_matiere, name='delete_matiere'),
    path('vue_etudiant/', views.vue_etudiant, name='vue_etudiant'),
    path('resultat_etudiant/', views.resultat_etudiant, name='result_etudiant'),
    path('affecter_matiere/', views.affecter_matiere, name='ajouter_matiere'),
    path('affecter_matiere_save', views.affecter_matiere_save, name='ajouter_matiere_save'),
    path('add_session/', views.add_session, name='add_session'),
    path('add_session_save', views.add_session_save, name='add_session_save'),
    path('manage_session/', views.manage_session, name='manage_session'),
    path('delete_session/<str:ses_id>', views.delete_session, name='delete_session'),
    path('edit_session/<str:ses_id>', views.edit_session, name='edit_session'),
    path('edit_session_save/', views.edit_session_save, name='edit_session_save'),
    path('transferer_etudiant/', views.transferer_etudiant, name='transferer_etudiant'),
    path('transferer_etudiant_save/', views.transferer_etudiant_save, name='transferer_etudiant_save'),
    path('emploi_temps/', views.plan, name='plan'),
    path('emploi_temps_save/', views.plan_save, name='plan_save'),
    path('manage_emploi/', views.manage, name='manage_emploi'),


    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
