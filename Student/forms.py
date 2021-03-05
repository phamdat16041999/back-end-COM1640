from django import forms
from Login.models import Data

class DataForm(forms.ModelForm):
	class Meta:
		model = Data
		fields = ('idData','Data')