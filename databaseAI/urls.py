from django.urls import path,include
from databaseAI import views
#from databaseAI import sun



urlpatterns = [
    
    path('',views.about),
    path('about',views.about),
    path('form',views.form),
    path('edit/<person_id>',views.edit),
    path('delete/<person_id>',views.delete),
    path('text',views.text),
    path('lobby',views.lobby),
    path('videolive',views.videolive),
    
    
    
]
