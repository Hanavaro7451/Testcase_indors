from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import Owner, Message

admin.site.register(Owner, UserAdmin)
admin.site.register(Message)
