from django.shortcuts import render,redirect
from django.http import HttpResponse 
from databaseAI.models import Person,AImodel
from django.contrib import messages
from django.http.response import StreamingHttpResponse
#from databaseAI.camera import VideoCampera,PredictSign
import time
from .models import Todo 
import os
# Create your views here.

def index(request):
    name = "Sun"
    age = 22
    all_person = Person.objects.all()
    return render(request,"index.html",{"name":name,"age":age,"all_Person":all_person})
def about(request):
    return render(request,"about.html")
def form(request):
    if request.method == "POST":
        #รับข้อมูล
        name = request.POST["name"]
        age =  request.POST["age"]
        print( name , age )
        print(type(age))
        #int(age)
        #บันทึกข้อมูล
        person=Person.objects.create(
            name1=name,
            age=age
        )
        person.save()
        messages.success(request,"บันทึกข้อมูลเรียบร้อย")
        #เปลี่ยนเส้นทาง
        return redirect("/")
    else :
         return render(request,"form.html")
    
def edit(request,person_id):
    if request.method =="POST":
        person = Person.objects.get(id=person_id)
        person.name1 =request.POST["name"]
        person.age = request.POST["age"]
        person.save()
        messages.success(request,"อัพเดตข้อมูลเรียบร้อย")
        #เปลี่ยนเส้นทาง
        return redirect("/")
    else:
        #ดึงข้อมูลเพื่อแก้ไข
        persone = Person.objects.get(id=person_id)
        return render(request,"edit.html",{"persone":persone})
    
def delete(request,person_id):
    person = Person.objects.get(id=person_id)
    person.delete()
    messages.success(request,"ลบข้อมูลเรียบร้อบ")
    return redirect("/")
        
     
    
    

def text(request):
    
    return render(request,"sun.txt")


def lobby(request):
    
    return render(request, 'chat/lobby.html')

def videolive(request):
    
    return render(request, 'chat/videolive.html')


            




#def Testfile(request):
