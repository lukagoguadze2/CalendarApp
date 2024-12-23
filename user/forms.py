from django.contrib.auth.forms import UserCreationForm

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django_select2.forms import Select2Widget

from universities.models import University, Faculty, Course
from user.models import User
from user.validators import validate_phone_number


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'email', 'identifier', 'first_name', 'last_name',
            'password1', 'password2'
        )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def clean_identifier(self):
        identifier = self.cleaned_data.get('identifier')

        if not identifier.isdigit():
            raise ValidationError('The identifier must be composed of digits only.')

        return identifier


class SecondStageRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'university', 'level_of_study', 'faculty', 'year_of_study', 'is_private',
        )

    university = forms.ModelChoiceField(
        queryset=University.objects,
        widget=Select2Widget(attrs={'class': 'form-control', 'placeholder': 'University', 'id': 'id_university'})
    )

    level_of_study = forms.ChoiceField(
        choices=Course.degree_level_choice,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_level_of_study'})
    )

    faculty = forms.ModelChoiceField(
        queryset=Faculty.objects,  # Initially empty
        widget=Select2Widget(attrs={'class': 'form-control', 'placeholder': 'Faculty', 'id': 'id_faculty'})
    )

    year_of_study = forms.IntegerField(
        min_value=1,
        max_value=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Year of Study'}),
    )

    is_private = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'm-1'}),
        label='Keep my profile private'
    )

    def clean_year_of_study(self):
        level_of_study = self.cleaned_data.get('level_of_study')
        if level_of_study == 'B' and self.cleaned_data.get('year_of_study') > 5:
            raise ValidationError('Invalid year of study for Bachelor degree.')
        elif level_of_study == 'M' and self.cleaned_data.get('year_of_study') > 2:
            raise ValidationError('Invalid year of study for Master degree.')

        return self.cleaned_data.get('year_of_study')


class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        label="Email address",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("No user found with this email address.")

        return email


class UpdatePasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('password1', 'password2')

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="New password",
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm new password"
    )

    def clean_password1(self):
        password = self.cleaned_data.get('password1')

        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long')

        if not any(char.isdigit() for char in password):
            raise ValidationError('Password must contain a digit')

        if not any(char.isalpha() for char in password):
            raise ValidationError('Password must contain a letter')

        if not any(char.isupper() for char in password):
            raise ValidationError('Password must contain an uppercase letter')

        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise ValidationError('Passwords do not match')

        return password2


class UpdateProfileForm(SecondStageRegistrationForm):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'phone_number', *SecondStageRegistrationForm.Meta.fields
        )

    phone_number = forms.CharField(
        max_length=20,
        validators=[validate_phone_number],
        help_text="Enter the phone number in international format, e.g., +123456789."
    )
