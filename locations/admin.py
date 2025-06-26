# locations/admin.py
from django.contrib import admin
from .models import State, County, City

admin.site.register(State)
admin.site.register(County)
admin.site.register(City)
