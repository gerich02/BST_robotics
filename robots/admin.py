from django.contrib import admin
from .models import Robot


@admin.register(Robot)
class RobotAdmin(admin.ModelAdmin):
    list_display = ('serial', 'model', 'version', 'created')
    search_fields = ('serial', 'model', 'version')
    list_filter = ('model', 'version')
