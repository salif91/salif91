from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from ecole.models import Ecole, Enseignant, Classe, Etudiant, GroupeScolaire, CustomUser, Personnel, Matiere, Note, Session, Resultat, Admin

#class UserModel(UserAdmin):
 #   list_display=('username', 'user_type')
admin.site.register( CustomUser, UserAdmin )

class EtudiantAdmin(admin.ModelAdmin):
    list_display=('admin','adresse', 'ecole', 'classe')
    search_fields=('admin', 'ecole', 'classe')
    
class SessionAdmin(admin.ModelAdmin):
    list_display=('debut', 'fin'  )
    search_fields=('debut',)  
    readonly_fields=('debut','fin')
admin.site.register(Session, SessionAdmin)    
admin.site.register(Etudiant, EtudiantAdmin)

class adminAdmin(admin.ModelAdmin):
    list_display=('admin', 'prenom')
admin.site.register(Admin, adminAdmin)
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