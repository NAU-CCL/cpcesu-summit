from django import forms
from .models import Project, File, Location, ProjectFiles


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_title', 'short_summary', 'status', 'partner',
                  'federal_agency', 'cesu_unit', 'description', 'budget',
                  'student_support', 'vet_support', 'location']
        widgets = {
            'project_title': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter project title here...'}),
        }

# Remove latter as it maybe redundant
# class ProjectFilesForm(forms.ModelForm):
#     class Meta:
#         model = ProjectFiles
#         fields = ['file']


class ProjectFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': True}),
        }


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name']
