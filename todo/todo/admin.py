from django.contrib import admin
from .models import ToDo

class AdminToDo(admin.ModelAdmin):
    list_display = ('id', 'title', 'start_date', 'end_date', 'task_date', 'user')

admin.site.register(ToDo, AdminToDo)