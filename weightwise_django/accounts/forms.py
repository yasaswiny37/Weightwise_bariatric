from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Patient


class PatientSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, required=True, label="Phone number")
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Date of birth"
    )
    gender = forms.ChoiceField(choices=[('', '---')] + Patient.GENDER_CHOICES, required=False)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'username',
            'phone_number', 'date_of_birth', 'gender',
            'password1', 'password2',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Patient.objects.create(
                user=user,
                phone_number=self.cleaned_data.get('phone_number', ''),
                date_of_birth=self.cleaned_data.get('date_of_birth'),
                gender=self.cleaned_data.get('gender', ''),
            )
        return user
