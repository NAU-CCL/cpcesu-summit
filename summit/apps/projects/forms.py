from django import forms

from .models import Project, File


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['p_num', 'project_title', 'short_summary', 'status', 'partner',
                  'federal_agency', 'cesu_unit', 'description', 'budget',
                  'student_support', 'vet_support']
        widgets = {
            'project_title': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter project title here...'}),
        }


class ProjectFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': True}),
        }
