from django import forms
from .models import *


class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = '__all__'
        widgets = {
            'branch_name': forms.TextInput(attrs={'placeholder': 'Branch Name', 'class': 'addbanktxt'}),
            'ifsc_code': forms.TextInput(attrs={'placeholder': 'IFSC Code', 'class': 'addbanktxt'}),
            'branch_address': forms.Textarea(attrs={'placeholder': 'Address', 'class': 'addbanktxtar'}),
            'branch_contact': forms.TextInput(attrs={'placeholder': 'Contact Number', 'class': 'addbanktxt'}),
        }


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        exclude = ['bank']
        fields = '__all__'
        widgets = {
            'account_no': forms.TextInput(attrs={'class': 'cstmrtxt'}),
            'account_holder': forms.TextInput(attrs={'class': 'cstmrtxt'}),
            'account_type': forms.TextInput(attrs={'class': 'cstmrtxt'}),
            'pancard_no': forms.TextInput(attrs={'class': 'cstmrtxt'}),
            'address': forms.Textarea(attrs={'class': 'cstmrtxtarea'}),
            'contact': forms.TextInput(attrs={'class': 'cstmrtxt'}),
        }


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        exclude = ['account', 'transaction_id']
        fields = '__all__'
        widgets = {
            'transaction_type': forms.Select(attrs={'class': 'cstmrtxt'}),
            'account_holder': forms.TextInput(attrs={'class': 'cstmrtxt'}),
            'amount': forms.TextInput(attrs={'class': 'cstmrtxt'}),
            'date': forms.DateInput(attrs={'class': 'cstmrtxt', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'cstmrtxt', 'type': 'time'}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'placeholder': 'Username', 'class': 'addbanktxt'}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(
        attrs={'placeholder': 'Password', 'class': 'addbanktxt'}))
