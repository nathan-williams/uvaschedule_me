from django import forms

class CourseForm(forms.Form):
    courses = forms.CharField(label="",
        max_length=1000,
        widget=forms.TextInput(attrs={'autofocus':'true', 'size':'80px', 'required':True, 'type':'text', 'style':'outline: 0; color: #000; text-align: center; padding: 4px; text-transform: uppercase; width:60%', 'name':'rcs'})
    )

class UpdateForm(forms.Form):
    courses = forms.CharField(label="",
        max_length=1000,
        widget=forms.TextInput(attrs={'autofocus':'true', 'size':'80px', 'type':'text', 'style':'outline: 0; color: #000; text-align:center; padding-top: 6px; padding-bottom: 5px; text-transform: uppercase; width:75%;'})
    )