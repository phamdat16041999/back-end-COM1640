from django import forms
from Login.models import Data

class DataForm(forms.ModelForm):
	class Meta:
		model = Data
<<<<<<< HEAD
		fields = ('idData','Data')
=======
		fields = ('idData','Data', 'Contribute')
>>>>>>> aecc2e6aa0344185093971c2eef33086382042f6
