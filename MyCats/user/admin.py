from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import Owner

admin.site.register(Owner, UserAdmin)
