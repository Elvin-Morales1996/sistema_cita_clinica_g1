from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class ActivityFilterForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    user = forms.ModelChoiceField(User.objects.all(), required=False)
    action = forms.CharField(max_length=150, required=False)
