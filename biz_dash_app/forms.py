from django import forms

from django.core.exceptions import ValidationError

from .models import CustomUser , Report

import re


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'manager','password']

    

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Regular expression for validating an Email
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValidationError("Invalid email format")
        return email


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['name', 'address', 'phone_number', 'id_proof', 'comment']

    


