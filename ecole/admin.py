from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from ecole.models import Ecole, Enseignant, Classe, Etudiant, GroupeScolaire, CustomUser, Personnel, Matiere, Note, Session, Resultat

class UserAdmin(UserAdmin):
    list_display=('first_name','last_name', 'username', 'email','user_type','is_staff', 'is_superuser', 'last_login', )
    search_fields=('first_name','last_name')
admin.site.register(CustomUser,  UserAdmin)

class EtudiantAdmin(admin.ModelAdmin):
    list_display=('admin','adresse', 'ecole', 'classe')
    search_fields=('admin', 'ecole', 'classe')
    readonly_fields=('admin', 'adresse','ecole', 'classe')
class SessionAdmin(admin.ModelAdmin):
    list_display=('debut', 'fin'  )
    search_fields=('debut',)  
    readonly_fields=('debut','fin')
admin.site.register(Session, SessionAdmin)    
admin.site.register(Etudiant, EtudiantAdmin)

class EcoleAdmin(admin.ModelAdmin):
    list_display=('nom', 'ville')
    
    list_per_page=5
admin.site.register(Ecole, EcoleAdmin)     

class PersonnelAdmin(admin.ModelAdmin):
    list_display=('admin', 'adresse','telephone', 'ecole',  )
    list_per_page=5
    
admin.site.register(Personnel, PersonnelAdmin)

class MatiereAdmin(admin.ModelAdmin):
    list_display=('nom', 'classe','personnel')
    readonly_fields=('nom','classe','personnel')
admin.site.register(Matiere, MatiereAdmin)  

class ResultatAdmin(admin.ModelAdmin):
    list_display=('etudiant','matiere', 'noteclass', 'noteexam')
    readonly_fields=('etudiant', 'matiere', 'noteclass', 'noteexam')

admin.site.register(Resultat, ResultatAdmin)    
#class MatiereAdmin(admin.ModelAdmin):
  #  list_display=('nom', 'classe', 'note')
   # list_per_page=5
#admin.site.register(Matiere, MatiereAdmin)    

#class NoteAdmin(admin.ModelAdmin):
  #  list_display=('moyenne',)
#admin.site.register(Note, NoteAdmin)    