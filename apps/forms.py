from django import forms
from .models import Profile
from django import forms
from .models import Notification, User
from .models import CrimeReport


class CrimeReportForm(forms.ModelForm):
    date_and_time = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        })
    )

    # type_of_crime = forms.ChoiceField(
    #     choices=CrimeReport.CRIME_TYPES,
    #     widget=forms.Select(attrs={
    #         'class': 'form-control'
    #     })
    # )

    class Meta:
        model = CrimeReport
        fields = ['type_of_crime', 'date_and_time', 'location', 'description', 'evidence']

class ProfileForm(forms.ModelForm):
    birth_date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )

    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date', 'picture']


class NotificationForm(forms.ModelForm):
    select_all_users = forms.BooleanField(required=False)

    class Meta:
        model = Notification
        fields = ['user', 'title', 'content', 'select_all_users']
