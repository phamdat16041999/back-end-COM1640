from django.contrib import admin
from .models import User, Faculty

class UserAdmin(admin.ModelAdmin):
	list_display = ['username', 'first_name','last_name']
	list_filter = ['Faculty']
	search_fields = ['username']
admin.site.register(User, UserAdmin)

class FacultyAdmin(admin.ModelAdmin):
	list_display = ['Name', 'Description','ClosureDate','FinalClosureDate']
	list_filter = ['Name']
	search_fields = ['Name']
admin.site.register(Faculty, FacultyAdmin)