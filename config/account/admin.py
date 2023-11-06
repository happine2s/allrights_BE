from django.contrib import admin
from .models import User
from django.contrib.auth.models import Group

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm

class UserAdmin(BaseUserAdmin):
    form=UserChangeForm
    add_form=UserCreationForm

    list_display=('userid','username','bio','img','is_active','is_admin')
    list_filter=('is_admin',)
    fieldsets=(
        (None, {'fields':('userid','password')}),
        ('User info',{'fields':('username','img','bio')}),
        ('Permissions',{'fields':('is_admin',)})
    )

    add_fieldsets=(
        (None,{
            'classes':('wide',),
            'fields':('userid','usernmae','password')
        })
    )
    search_fields=('userid',)
    ordering=('userid',)
    filter_horizontal=()

admin.site.register(User,UserAdmin)
admin.site.unregister(Group)