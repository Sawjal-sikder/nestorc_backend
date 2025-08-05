from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.http import HttpResponse
from django.urls import path, reverse
from django.utils.html import format_html
from django.shortcuts import redirect

from .models import CustomUser, PasswordResetCode
from .pdf_export import download_user_pdf, download_all_users_pdf
from .excel_export import download_all_users_excel

# Form to create new users in admin
class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ("email",)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# Form to change existing users in admin
class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this user's password, "
            "but you can change the password using <a href=\"../password/\">this form</a>."
        ),
    )

    class Meta:
        model = CustomUser
        fields = "__all__"


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    actions = [download_user_pdf]

    list_display = ("full_name", "phone_number", "email", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("full_name", "phone_number")}),  
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_active"),
        }),
    )
    search_fields = ("email", "full_name")
    ordering = ("email",)

    def get_urls(self):
        """Add custom URLs for PDF and Excel downloads"""
        urls = super().get_urls()
        custom_urls = [
            path('download-all-pdf/', self.admin_site.admin_view(download_all_users_pdf), 
                 name='download_all_users_pdf'),
            path('download-all-excel/', self.admin_site.admin_view(download_all_users_excel), 
                 name='download_all_users_excel'),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        """Add custom context to change list view"""
        extra_context = extra_context or {}
        extra_context['download_all_url'] = reverse('admin:download_all_users_pdf')
        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(CustomUser, CustomUserAdmin)


class PasswordResetCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at', 'is_used', 'is_expired_display')
    list_filter = ('is_used', 'created_at')
    search_fields = ('user__email', 'code')

    def is_expired_display(self, obj):
        return obj.is_expired()
    is_expired_display.boolean = True
    is_expired_display.short_description = 'Expired?'

admin.site.register(PasswordResetCode, PasswordResetCodeAdmin)