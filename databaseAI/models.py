from django.db import models

# Create your models here.
class Person(models.Model):
    name1 = models.CharField(max_length=100)
    age = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name1 + " "+str(self.age)
    
class AImodel(models.Model):
    AIfile = models.FileField()

class Todo(models.Model): 
    task = models.CharField(max_length=200) 
  
    def __str__(self): 
        return f"{self.task}"
    