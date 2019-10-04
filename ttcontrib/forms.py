from django import forms

class Search(forms.Form):
    Repository_Link = forms.CharField()