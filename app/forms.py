from django import forms

class ImageForm(forms.Form):
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
