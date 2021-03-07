from django.contrib import admin
from .models import User, Faculty, Term, Contribute, Data, Comment
class UserAdmin(admin.ModelAdmin):
	list_display = ['username', 'first_name','last_name']
	list_filter = ['Faculty']
	search_fields = ['username']
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
	list_display = ['Name', 'Date','Status','Document']
	list_filter = ['Name']
	search_fields = ['Name']
admin.site.register(Contribute, ContributeAdmin)
class DataAdmin(admin.ModelAdmin):
	list_display = ['Data', 'ContributeID']
	list_filter = ['Data']
	search_fields = ['Data','ContributeID']
admin.site.register(Data, DataAdmin)
class CommentAdmin(admin.ModelAdmin):
	list_display = ['Contribute', 'User','Comment','DateComment']
	list_filter = ['Contribute']
	search_fields = ['Contribute']
admin.site.register(Comment, CommentAdmin)