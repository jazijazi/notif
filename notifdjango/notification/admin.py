from django.contrib import admin
from .models import Notification , Group


#admin.site.register(Notification)
#admin.site.register(Group)

@admin.register(Notification)
class Notification(admin.ModelAdmin):
    list_display = ('title','creator','seenCounts','group')
    list_filter = ('group' , 'date_created')

@admin.register(Group)
class Group(admin.ModelAdmin):
    list_display = ('name','num_active')