from django.contrib import admin
from databaseAI.models import Person,AImodel
from .models import *

# Register your models here.
admin.site.register(Person)
admin.site.register(AImodel)
admin.site.register(Todo)