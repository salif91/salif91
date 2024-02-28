from django.shortcuts import render, redirect
from django.contrib.auth.models import auth,  User
from.forms import LoginForm, AddSchoolForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from ecole.models import Ecole, Etudiant, CustomUser, Classe, Matiere, Personnel, Session, Resultat, EmploiDuTemps
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail
from django.contrib.auth.decorators import user_passes_test
from functools import wraps
from django.http import HttpResponseForbidden
from django.core.cache import cache
from django.contrib.auth import logout
from django.views.decorators.vary import vary_on_cookie
import random
import string


def user_type_required(user_type):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.user_type == user_type:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("vous n'etes pas Autorisé à acceder ici")
        return _wrapped_view
    return decorator

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
           
       
        if user is not None:
            auth.login(request, user)
            user_type = user.user_type
            if user.user_type == '1':
                return redirect('adminpage')
            elif user.user_type =='2':
                return redirect('add_result')    
            elif user.user_type == '3':
                return redirect('vue_etudiant')
            else:
                return redirect('adminpage')
           
        else:
            messages.error(request,"identifiants erronés",)
            return render(request,'login/login.html',)
    else:
     return render(request,'login/login.html',)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    logout(request)
    # Autres opérations de déconnexion si nécessaire
    return redirect('login')

def index(request):
    user = request.user
    return render(request,'login/index.html',{'user':user})

def register(request):
    if request.method=='POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password!= password2:
            messages.error(request,"les mots de passe ne correspondent pas")
        email = request.POST.get('email')
        data = User.objects.create_user(first_name= first_name, last_name= last_name ,username=username,password=password,email=email,) 
        data.save()
    return render(request, 'login/register.html',)


def dashboard(request):
    return render(request, 'login/school_dashbord.html',)

@user_type_required('1')
def list_etudiant_par_classe(request, id):
    e= Etudiant.objects.filter(classe=id)
    return render(request, 'admin_template/list_etudiant_par_classe.html', {'e':e})
@user_type_required('1')
def edit_student(request, student_id):
    ecoles = Ecole.objects.all()
    classes = Classe.objects.all()
    student= Etudiant.objects.get(admin=student_id)
    return render(request, 'admin_template/edit_student.html', {'student':student, 'ecoles':ecoles, 'classes':classes})


def edit_personnel(request,pers_id):
    ecole =Ecole.objects.all()
    personnel= Personnel.objects.get(admin=pers_id)
    return render(request, 'admin_template/edit_personnel.html', {'personnel':personnel, 'ecole':ecole})

@user_type_required('1')
def delete_personnel(request,pers_id):
    personnel=CustomUser.objects.get(id=pers_id)
    personnel.delete()
    return redirect('manage_personnel')


def edit_personnel_save(request):
    if request.method == 'POST':
        pers_id = request.POST.get('pers_id',)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        adresse = request.POST.get('adresse') 
        telephone = request.POST.get('telephone')
        
        ecole = request.POST.get('ecole')
        try:

            user= CustomUser.objects.get(id= pers_id)
            user.first_name=first_name
            user.last_name=last_name
            user.username=username
            user.email=email
            user.save()

            personnel=Personnel.objects.get(admin= pers_id)
            personnel.adresse=adresse
            personnel.telephone=telephone
           
            ecole_obj= Ecole.objects.get(id=ecole)
            personnel.ecole=ecole_obj
            personnel.save()
            messages.success(request, "enseignant modifié avec succès")
            return redirect('manage_personnel')

        except:
            messages.error(request, "modification echoué")
            return redirect('manage_personnel')
@user_type_required('2')            
@login_required()   
def personnel_add_result(request):
    matiere= Matiere.objects.filter(personnel= request.user.id)
    session = Session.objects.all()
    classe_list=[]
    for m in matiere:
        classe= Classe.objects.get(id=m.classe.id)
        classe_list.append(classe.id)
    final_classe= []
    for classe in classe_list:
        if classe not in final_classe:
            final_classe.append(classe)    
    student= Etudiant.objects.filter(classe__in=final_classe)
    return render(request, 'admin_template/add_result.html', {'matiere':matiere, 'session':session, 'student': student})

def save_result(request):
    if request.method == 'POST':
        student= request.POST.get('student')
        matiere= request.POST.get('matiere')
        
        noteclass= request.POST.get('noteclass')
        noteexam= request.POST.get('noteexam')
        session= request.POST.get('session')
        student_obj=Etudiant.objects.get(id=student)
        matiere_obj=Matiere.objects.get(id=matiere)
        verif_exist= Resultat.objects.filter(matiere=matiere_obj, etudiant= student_obj).exists() 
        if verif_exist:
           result = Resultat.objects.get(matiere= matiere_obj, etudiant= student_obj)
           result.noteclass=noteclass
           result.noteexam=noteexam
           result.save()
           messages.success(request,"resultat de l'etudiant modifié avec succès")
           return redirect ('add_result')
        else:
            result = Resultat(matiere= matiere_obj, etudiant= student_obj, noteclass=noteclass, noteexam=noteexam)
            result.save()
            messages.success(request,"resultat de l'etudiant ajouté avec succès")
            return redirect ('add_result')
    else:
        return HttpResponse('impossible')
   

def edit_student_save(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id',)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        adresse = request.POST.get('adresse') 
        telephone = request.POST.get('telephone')
        classe = request.POST.get('classe')
        ecole = request.POST.get('ecole')
        try:

            user= CustomUser.objects.get(id= student_id)
            user.first_name=first_name
            user.last_name=last_name
            user.username=username
            user.email=email
            user.save()

            student=Etudiant.objects.get(admin=student_id)
            student.adresse=adresse
            student.telephone=telephone
            classe_obj= Classe.objects.get(id=classe)
            student.classe=classe_obj
            ecole_obj= Ecole.objects.get(id=ecole)
            student.ecole=ecole_obj
            student.save()
            messages.success(request, "etudiant modifié avec succès")
            return redirect('manage_student')
        except:
            messages.error(request, "modification echoué")
            return redirect('manage_student')

@login_required()
@user_type_required('3')
def vue_etudiant(request):
    student = Etudiant.objects.get(admin=request.user.id)
    
    return render(request, 'etudiant_template/vue_etudiant.html', {'student': student})

def resultat_etudiant(request):
    etudiant = Etudiant.objects.get(admin=request.user.id) 
    re= Resultat.objects.filter(etudiant=etudiant) 
    return render(request, 'etudiant_template/note_etudiant.html', {'re':re})


@user_type_required('1')
def manage_student(request):
    students= Etudiant.objects.all()
    return render(request, 'admin_template/manage_student.html', {'students': students})

@user_type_required('1')
@login_required()
def manage_classe(request):
    classes= Classe.objects.all()
    return render(request, 'admin_template/manage_classe.html', {'classes': classes})







@user_type_required('1')
def add_student_save(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        adresse = request.POST.get('adresse')
        telephone = request.POST.get('telephone')
        ecole= request.POST.get('ecole')
        classe= request.POST.get('classe')
        session= request.POST.get('session')
        profile_pic= request.FILES.get('profile_pic')
        
    
      #  try:
        user = CustomUser.objects.create_user(first_name= first_name, last_name= last_name ,username=username,password=password,email=email, user_type='3')
        user.etudiant.adresse=adresse
        user.etudiant.telephone=telephone
       
        ecole_obj= Ecole.objects.get(id = ecole)
        user.etudiant.ecole=ecole_obj
        classe_obj= Classe.objects.get(id= classe)
        user.etudiant.classe=classe_obj
        session_obj= Session.objects.get(id=session)
        user.etudiant.session=session_obj
        user.etudiant.profile_pic=profile_pic
        user.save()

        send_mail(
           subject= 'Inscription ',
           message=" votre inscription a bien été pris en compte, voici vos cordonnées pour vous identifier sur systeme " + 'username = '+user.username ,
           from_email='salifsorytra@gmail.com',
           recipient_list=[email,],
           )

        messages.success(request, 'Etudiant ajoutée')
        return redirect('add_student')
           
    else:
           messages.error(request, 'Etudiant non ajoutée')
           return redirect('add_student')

@user_type_required('1')
def edit_matiere(request, mat_id):
    matiere= Matiere.objects.get(id=mat_id)
    classe= Classe.objects.all()
    pers= CustomUser.objects.filter(user_type=2)
    return render(request, 'admin_template/edit_matiere.html',{'matiere':matiere, 'classe':classe, 'pers':pers})
@login_required()
def delete_matiere(request, mat_id):
    matiere = Matiere.objects.get(id=mat_id)
    matiere.delete()
    messages.success(request,"Matière suprimer avec succes")
    return redirect('manage_matiere')



def edit_matiere_save(request):
    if request.method == 'POST':
        mat_id = request.POST.get('mat_id')
        nom= request.POST.get('nom')
        personnel=request.POST.get('personnel')
        classe=request.POST.get('classe')
        try:
            matiere= Matiere.objects.get(id=mat_id)
            matiere.nom=nom
            personnel=CustomUser.objects.get(id=personnel)
            matiere.personnel= personnel
            classe = Classe.objects.get(id=classe)
            matiere.classe= classe
            matiere.save()
            return redirect('manage_matiere')
        except:
            
            return HttpResponse("non modifié")


def affecter_matiere(request):
    classe = Classe.objects.all()
    pers= CustomUser.objects.filter(user_type='2')
    return render(request, 'admin_template/ajouter_matiere.html', {'classe':classe, 'pers':pers, })

def affecter_matiere_save(request):
    if request.method == 'POST':
        matiere = request.POST.get('matiere')
        classe = request.POST.get('classe')
        classeobj= Classe.objects.get(id=classe)
        personnel = request.POST.get('personnel')
        personnelobj= CustomUser.objects.get(id=personnel)
        try:
            matiere= Matiere(nom=matiere, personnel=personnelobj, classe=classeobj)
            matiere.save()
            messages.success(request,'Affectation reussie')    
        except:
            return HttpResponse('impossible')
    return redirect('ajouter_matiere')           

def add_matiere(request):
    
    return render(request, 'admin_template/add_matiere.html', )
def add_matiere_save(request):
    if request.method == 'POST':
        nom= request.POST.get('nom')
        
        try:
            matiere= Matiere(nom=nom, )
            matiere.save()
            messages.success(request,"Matière ajoutée avec succès")
            return redirect('add_matiere')
        except:
            messages.error(request, "Matière non ajoutée")
            return redirect('add_matiere')

@login_required
@user_type_required('1')
def manage_matiere(request):
    matiere= Matiere.objects.all() 
    return render(request,'admin_template/manage_matiere.html', {'matiere':matiere})   
@user_type_required('1')
def manage_personnel(request):
    personnel = Personnel.objects.all()
    return render(request, 'admin_template/manage_personnel.html',{'personnel':personnel})
@user_type_required('1')
def add_personnel(request):
    ecole= Ecole.objects.all()
    matiere=Matiere.objects.all()
    classe = Classe.objects.all()
    return render(request, 'admin_template/add_personnel.html',{'ecole':ecole, 'matiere':matiere, 'classe':classe})     

def add_personnel_save(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        adresse = request.POST.get('adresse')
        telephone = request.POST.get('telephone')
        ecole= request.POST.get('ecole')
        
        try:
            user=CustomUser.objects.create_user(first_name= first_name, last_name= last_name ,username=username,password=password,email=email, user_type='2')
            user.personnel.adresse=adresse
            user.personnel.telephone=telephone
            ecole_objpers=Ecole.objects.get(id=ecole)
            user.personnel.ecole=ecole_objpers
            
            user.save()
            messages.success(request, 'Enseignant ajouté avec succès')
            return redirect('add_personnel')
        except:
            messages.error(request, 'Enseignant non ajouté')
            return redirect('add_personnel')    
@user_type_required('1')
def add_classe(request):
    return render(request, 'admin_template/add_classe.html',)

def add_classe_save(request):
    if request.method == 'POST':
        nom=request.POST.get('nom')
        try:
            data = Classe(nom=nom)
            data.save()
            messages.success(request, 'Classe ajoutée')
            return redirect('add_classe')
        except:
            messages.error(request, 'Classe non ajoutée')
            return redirect('add_classe')    

def userdetails(request):
    if request.user != None:
      return HttpResponse("user : " + request.user.username +"type : " + request.user.user_type )
    else:
        return HttpResponse("login first")      
# Create your views here.


@cache_control(no_cache=True, max_age=0,must_revalidate=True)
@login_required()
def admin_page(request):
    if request.user.user_type != '1':
        return HttpResponse('Accès interdit ici')  
    else:    
        nb_classe = Classe.objects.all().count
        nb_etudiant= Etudiant.objects.all().count
        nb_personnel=Personnel.objects.all().count
        nb_matiere=Matiere.objects.all().count
        return render(request, 'admin_template/home_content.html', {'nb_classe': nb_classe, 'nb_etudiant': nb_etudiant, 'nb_personnel':nb_personnel,'nb_matiere':nb_matiere })

def add_school(request):
    return render(request, 'admin_template/add_school.html')
@login_required()
@user_type_required('1')
def add_student(request):
    classes = Classe.objects.all()
    sessions=Session.objects.all()
    ecoles = Ecole.objects.all()
    return render(request, 'admin_template/add_student.html', {'ecoles':ecoles, 'classes':classes, 'sessions':sessions})


def add_school_save(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        ville = request.POST.get('ville')
        try:
            data = Ecole(nom=nom,  ville=ville)
            data.save()
            messages.success(request, 'Ecole ajoutée')
            return redirect('add_school')  
        except:
            messages.error(request, 'Ecole non ajoutée')
            return redirect('add_school')
    else:
        return HttpResponse("non autorise") 

@user_type_required('1')
def add_session(request):
    return render(request, 'admin_template/add_session.html')

def add_session_save(request):
    if request.method == 'POST':
        intitule= request.POST.get('intitule')
        debut=request.POST.get('debut')
        fin= request.POST.get('fin')
        try:
            session= Session(intitule=intitule, debut=debut, fin=fin)
            session.save()
            messages.success(request, 'la session crée avec succès')
            return redirect('add_session')
        except:
            messages.error(request, 'Impossible de créer la session')
            return redirect('add_session')
@user_type_required('1')
def manage_session(request):
    sessions= Session.objects.all()
    return render(request, 'admin_template/manage_session.html', {'sessions': sessions})
@user_type_required('1')
def delete_session(request, ses_id):
    session = Session.objects.get(id=ses_id)
    session.delete()
    return redirect('manage_session')

@user_type_required('1')
def edit_session(request,ses_id):
    session= Session.objects.get(id=ses_id)
    return render(request, 'admin_template/edit_session.html', {'session': session})

#modification d'une session
@user_type_required('1')
def edit_session_save(request):
    if request.method == 'POST':
        ses_id= request.POST.get('ses_id')
        intitule= request.POST.get('intitule')
        debut= request.POST.get('debut')
        fin= request.POST.get('fin')
        try:
          session= Session.objects.get(id=ses_id)
          session.intitule= intitule
          session.debut= debut
          session.fin= fin
          session.save()
          messages.success(request, 'session modifiée avec succès')
          return redirect('manage_session')
        except:
            messages.error(request,'session non modifiée')  
            return redirect('manage_session')

#vue de transfert dun etudiant
@user_type_required('1')
def transferer_etudiant(request):
    students= Etudiant.objects.all()
    sessions= Session.objects.all()
    classes= Classe.objects.all()
    return render(request, 'admin_template/transferer_etudiant.html', {'students': students, 'sessions': sessions, 'classes': classes})

#multi-transfert des etudiant vers une classe 
@user_type_required('1')
def transferer_etudiant_save(request):
    if request.method == 'POST':
        student= request.POST.getlist('student')
        
        classe= request.POST.get('classe')
        classe_obj= Classe.objects.get(id=classe)
        session= request.POST.get('session')
        session_obj= Session.objects.get(id=session)
        for st_id in student:
            try:
                student_obj= Etudiant.objects.get(id=st_id)
                student_obj.classe=classe_obj
                student_obj.session= session_obj
                student_obj.save()
            except Etudiant.DoesNotExist:
                messages.error(request, f'Étudiant avec ID {st_id} non trouvé.')   

        messages.success(request, 'Transfert effectué avec succès')
        return redirect('transferer_etudiant')

@user_type_required('1')
def plan(request):  
    
    matieres = Matiere.objects.all()
    classes = Classe.objects.all()
    return render(request, 'admin_template/emploi_temps.html', {'classes': classes, 'matieres': matieres, })

def plan_save(request):
    if request.method == 'POST':
        matiere= request.POST.get('matiere') 
        classe= request.POST.get('classe')
        jour= request.POST.get('jour')
        debut= request.POST.get('heure_debut')   
        fin= request.POST.get('heure_fin')
        
        matiere_obj= Matiere.objects.get(id=matiere)
        classe_obj= Classe.objects.get(id=classe)
        try:
            ep= EmploiDuTemps(matiere=matiere_obj,classe=classe_obj, jour=jour, heure_debut=debut, heure_fin=fin)
            ep.save()
            messages.success(request, 'Emploi du temps creer avec succès pour la classe ' +classe_obj.nom)
            return redirect('plan')
        except:
            messages.error (request, 'creation echoué')
    return redirect('plan')        
def manage(request):
    classes = Classe.objects.all()
   
    # Créer un dictionnaire pour stocker les emplois du temps par classe
    emplois_par_classe = {}

     # Remplir le dictionnaire avec les emplois du temps pour chaque classe    
    for classe in classes:
        emplois_du_temps = EmploiDuTemps.objects.filter(classe=classe)
        emplois_par_classe[classe] = emplois_du_temps

    # Passer les données au contexte du template
    context = {
        'emplois_par_classe': emplois_par_classe,
    }

    emplois_par_classe = {}
    return render(request, 'admin_template/manage_emploi.html', context)        
    
 