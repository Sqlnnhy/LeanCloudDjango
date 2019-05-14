from django import forms


class SaltForm(forms.Form):
    salt = forms.CharField()


class NameForm(forms.Form):
    salt = forms.CharField()
    userName = forms.CharField()
