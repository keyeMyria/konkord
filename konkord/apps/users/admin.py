from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import (
    AdminPasswordChangeForm, UserChangeForm, UserCreationForm,
)
from users.models import User, Email, Phone


class EmailInline(admin.TabularInline):
    model = Email
    extra = 0


class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None
    inlines = [EmailInline, PhoneInline]
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = (
        'username', 'email', 'phone', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = (
        'username',
        'first_name',
        'last_name',
        'emails__email',
        'phones__number'
    )
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

    def email(self, obj):
        email = obj.emails.order_by('-default').first()
        if email:
            return email.email
        return '-'

    def phone(self, obj):
        phone = obj.phones.order_by('-default').first()
        if phone:
            return phone.number
        return '-'
