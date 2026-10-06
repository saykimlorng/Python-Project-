from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser



admin.site.register(CustomUser)


# class CustomUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = CustomUser
#         fields = ('username', 'email', 'phone', 'address')


# class CustomUserChangeForm(UserChangeForm):
#     class Meta(UserChangeForm.Meta):
#         model = CustomUser
#         fields = '__all__'


# @admin.register(CustomUser)
# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     list_display = ('username', 'email', 'is_staff', 'is_active', 'date_joined')
#     list_filter = ('is_staff', 'is_superuser', 'is_active')
#     search_fields = ('username', 'email', 'phone')
#     ordering = ('username',)
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         ('Personal information', {'fields': ('email', 'phone', 'address')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'email', 'phone', 'address', 'password1', 'password2', 'is_active', 'is_staff'),
#         }),
#     )
