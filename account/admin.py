from django.contrib import admin
from account.models import User,Products , Category
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Register your models here.


class UserModelAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id','email', 'name', 'tc' ,'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'tc' , 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email','id')
    filter_horizontal = ()

admin.site.register(User, UserModelAdmin)

class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('id','name','price','category','created_at','updated_at','user')
    list_filter = ('category','created_at','updated_at')
    search_fields = ('name','price','category')
    ordering = ('name','price','category')
    filter_horizontal = ()

admin.site.register(Products,ProductModelAdmin)
admin.site.register(Category)