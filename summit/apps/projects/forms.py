from django import forms

from .models import Project, ProjectFiles


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_title', 'short_summary', 'status', 'partner',
                  'federal_agency', 'cesu_unit', 'description', 'budget',
                  'student_support', 'file']
        widgets = {
            'project_title': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter project title here...'}),
        }


class ProjectFilesForm(forms.ModelForm):
    class Meta:
        model = ProjectFiles
        fields = ['file']
