from django.contrib.auth.models import AbstractUser

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver



class CustomUser(AbstractUser):
    user_type_data=((1, 'admin'), (2, 'personnel'), (3, 'etudiant'))
    user_type = models.CharField(max_length=10, choices=user_type_data)
    


class Ecole(models.Model):
    nom= models.fields.CharField(max_length=200,verbose_name="nom ")
    
    ville= models.fields.CharField(max_length=200,)
   
    objects= models.Manager()
    
    class META:
     verbose_name = "Ecole"
     verbose_name_plural = "Ecoles"
    ordering = ["nom"]

    def __str__(self):
        return f'{self.nom}'
   

class Admin(models.Model):
    admin=models.OneToOneField(CustomUser, on_delete=models.CASCADE, )

   
    prenom = models.CharField(max_length=50)
    
    
    objects = models.Manager()



class Enseignant(models.Model):
    nom= models.fields.CharField(max_length=200,verbose_name="nom ")
    prenom= models.fields.CharField(max_length=200,verbose_name="prenom ")
    adresse= models.fields.CharField(max_length=200,verbose_name="adresse ")
    telephone= models.fields.CharField(max_length=12,verbose_name="telephone")
    def __str__(self):
        return f'{self.nom} {self.prenom}'
    class Meta:
        verbose_name = "Enseignant"
        verbose_name_plural = "Enseignants"
    ecole = models.ForeignKey(Ecole, on_delete=models.CASCADE) 
    classe= models.ForeignKey('Classe', on_delete=models.CASCADE)
    
    objects = models.Manager()   

class Classe(models.Model):
    nom = models.fields.CharField(max_length=200,verbose_name="nom ")
    
    objects = models.Manager()
    def __str__(self):
        return f'{self.nom}'

class Etudiant(models.Model):
    admin=models.OneToOneField(CustomUser, on_delete=models.CASCADE, )
    adresse= models.fields.CharField(max_length=200,verbose_name="adresse ")
    telephone= models.fields.CharField(max_length=12,verbose_name="telephone")
    classe=  models.ForeignKey(Classe, on_delete=models.CASCADE)
    ecole= models.ForeignKey(Ecole, on_delete=models.CASCADE)
    objects =models.Manager()
    def __str__(self):
        return f'{self.admin.first_name} {self.admin.last_name}'
        
    
class Personnel(models.Model):
    admin=models.OneToOneField(CustomUser, on_delete=models.CASCADE, )
    adresse= models.fields.CharField(max_length=200,verbose_name="adresse ")
    telephone= models.fields.CharField(max_length=12,verbose_name="telephone")
    ecole =models.ForeignKey(Ecole, on_delete=models.CASCADE, null=True)
    objects =models.Manager()

class Note(models.Model):
    moyenne = models.fields.DecimalField(max_digits=5, decimal_places=2)


    
class Matiere(models.Model):
    nom = models.fields.CharField(max_length=200,verbose_name="nom")
    classe= models.ForeignKey(Classe,on_delete=models.CASCADE)
    personnel= models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    
    objects = models.Manager()   
    
    
    
    def __str__(self):
        return f'{self.nom} '
    class Meta:
        verbose_name = "Matière"
        verbose_name_plural = "Matières"
    classe = models.ForeignKey(Classe, on_delete=models.SET_NULL, null=True)

class GroupeScolaire(models.Model):
    nom= models.fields.CharField(max_length=200,verbose_name="nom ")
    
    def __str__(self):
        return f'{self.nom}'    

class Session(models.Model):

    intitule= models.fields.CharField(max_length=500,verbose_name="intitule")
    debut= models.DateField(auto_now_add=True)
    fin=models.DateField(auto_now=True)

class Resultat(models.Model):
    etudiant=models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    matiere= models.ForeignKey(Matiere, on_delete=models.CASCADE)
    noteclass= models.FloatField(default=0)
    noteexam= models.FloatField(default=0)

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type==1:
            Admin.objects.create(admin=instance)
        if instance.user_type==2:
            Personnel.objects.create(admin=instance, telephone="", adresse="",  ecole=Ecole.objects.get(id=1))
        if instance.user_type==3:
            Etudiant.objects.create(admin=instance, adresse="", telephone="", classe=Classe.objects.get(id=1), ecole=Ecole.objects.get(id=1 )  )  


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance,  **kwargs):
    if instance.user_type==1:
        instance.admin.save()
    if instance.user_type==2:
        instance.personnel.save()
    if instance.user_type==3:
        instance.etudiant.save()


# Create your models here.
