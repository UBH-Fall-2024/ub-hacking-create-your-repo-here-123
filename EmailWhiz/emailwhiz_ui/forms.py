from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    linkedin_url = forms.URLField(max_length=200, required=True)
    email = forms.EmailField(max_length=100, required=True)  # New Email field
    graduated_or_not = forms.ChoiceField(
        choices=[('yes', 'Yes'), ('no', 'No')],
        required=True
    )  # New Graduated field
    college = forms.CharField(max_length=200, required=False)  # New College field (optional)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'linkedin_url', 'email', 'graduated_or_not', 'college', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        graduated = cleaned_data.get('graduated_or_not')
        college = cleaned_data.get('college')

        # If graduated is 'yes', ensure that college is provided
        if graduated == 'yes' and not college:
            self.add_error('college', 'This field is required when you select "Yes" for graduation.')

        return cleaned_data
