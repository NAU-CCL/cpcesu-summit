from django import forms

from .models import Project, File, Location


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['budget',
                  'cesu_unit',
                  'description', 'discipline',
                  'federal_agency', 'field_of_science', 'final_report', 'fiscal_year',
                  'init_start_date',
                  'location',
                  'mod_desc', 'mod_num', 'mod_type', 'monitoring',
                  'notes', 'num_of_students',
                  'p_num', 'partner', 'pp_i', 'project_manager', 'project_title',
                  'r_d',
                  'sci_method', 'sensitive', 'short_summary', 'src_of_funding', 'staff_member', 'status',
                  'student_support',
                  'tech_rep', 'tent_end_date', 'tent_start_date', 'type',
                  'vet_support']
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


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name']
