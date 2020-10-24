from django.contrib import admin
from .models import pubKeys

# Register your models here.

admin.site.register(pubKeys)

# list_display = ['pk', 'text', 'text_note']