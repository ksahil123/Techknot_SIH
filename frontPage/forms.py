from django import forms

class addressForm(forms.Form):
	origin = forms.CharField()
	destination = forms.CharField()


