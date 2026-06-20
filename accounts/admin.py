from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ('Campus Info', {'fields': ('college_email', 'campus', 'graduation_year', 'major', 'bio', 'avatar')}),
    )
    list_display = ['username', 'email', 'college_email', 'campus', 'is_staff']


admin.site.register(User, CustomUserAdmin)