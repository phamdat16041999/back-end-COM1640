from django.contrib import admin
from .models import User, Faculty, Term, Contribute, Data, Comment
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm
class UserAdmin(BaseUserAdmin):
	add_form = UserCreationForm
	list_display = ['username', 'first_name','last_name','Faculty', 'Sex']
	list_filter = ['Faculty']
	search_fields = ['username']
	fieldsets = BaseUserAdmin.fieldsets  +(
		(None, {
			'fields': ('Faculty', 'Sex')
		}),
		# ('Advanced options', {
		# 	'classes': ('collapse',),
		# 	'fields': ('registration_required', 'template_name'),
		# }),
	)
admin.site.register(User, UserAdmin)

class FacultyAdmin(admin.ModelAdmin):
	list_display = ['Name', 'Description']
	list_filter = ['Name']
	search_fields = ['Name']
admin.site.register(Faculty, FacultyAdmin)
class TermAdmin(admin.ModelAdmin):
	list_display = ['NameTerm', 'Description','ClosureDate','FinalClosureDate']
	list_filter = ['NameTerm']
	search_fields = ['NameTerm']
admin.site.register(Term, TermAdmin)
class ContributeAdmin(admin.ModelAdmin):
	list_display = ['Name', 'Date','Status','Document','UserID']
	list_filter = ['Name']
	search_fields = ['Name']
	Readed = ['Name']
admin.site.register(Contribute, ContributeAdmin)
class DataAdmin(admin.ModelAdmin):
	list_display = ['Data', 'ContributeID']
	list_filter = ['Data']
	search_fields = ['Data','ContributeID']
admin.site.register(Data, DataAdmin)
class CommentAdmin(admin.ModelAdmin):
	list_display = ['ContributeID', 'UserID','Comment','DateComment']
	list_filter = ['ContributeID']
	search_fields = ['ContributeID']
admin.site.register(Comment, CommentAdmin)