from django.contrib import admin

from .models import User, userProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role', 'is_active', 'is_admin')
    list_display_links = ('id', 'username', 'email')
    ordering = ('-date_joined',)
    search_fields = ('email', 'username',)
    list_editable = ('is_admin',)
    actions = ('revoke', 'promoting')
    fieldsets = ( 
        ('user', {'fields': ('username', 'email', 'password', 'role')}),
        ('personal info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_superadmin')}),
    )
    
    def revoke(self, request, queryset):
        queryset.update(is_active=False)
        
    def promote(self, request, queryset):
        queryset.update(is_active=True)
        

@admin.register(userProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'province', 'city', 'zipcode')
    list_display_links = ('id', 'user')
    search_fields = ('user',)
    fieldsets = ( 
        ('user', {'fields': ('user',)}),
        ('pictures', {'fields': ('profile_picture', 'cover_photo')}),
        ('location', {'fields': ('province', 'city', 'zipcode')}),
        ('address', {'fields': ('first_address', 'second_address')}),
    )