from django import forms

from school_profiles.models import ParentProfile, StudentProfile, TeacherProfile


class ParentProfileForm(forms.ModelForm):
    class Meta:
        model = ParentProfile
        fields = '__all__'


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})  # TODO: Use calendar from Semantic-UI
        }


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = '__all__'
