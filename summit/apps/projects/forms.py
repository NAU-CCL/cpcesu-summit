from django import forms

from .models import Project, File, Location, Modification


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['budget', 'cesu_unit', 'description', 'discipline', 'federal_agency', 'field_of_science',
                  'final_report', 'fiscal_year', 'init_start_date', 'location',
                  'monitoring', 'notes', 'num_of_students','p_num', 'partner', 'pp_i', 'project_manager',
                  'project_title', 'r_d', 'sci_method', 'sensitive', 'short_summary', 'src_of_funding', 'staff_member',
                  'status', 'student_support', 'tech_rep', 'tent_end_date', 'tent_start_date', 'type', 'vet_support']
        widgets = {
            'project_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title here...'}),
            'p_num': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter P-Num here...'}),
            'short_summary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Quick details...'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter here...'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter here...'}),
            'status': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'partner': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'federal_agency': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'pp_i': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'project_manager': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'tech_rep': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'location': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'student_support': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'num_of_students': forms.NumberInput(attrs={'class': 'form-control'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control'}),
            'fiscal_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'vet_support': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'cesu_unit': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'staff_member': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'discipline': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'r_d': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'src_of_funding': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'field_of_science': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'type': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'sensitive': forms.CheckboxInput(attrs={'class': 'custom-control custom-checkbox'}),
        }


class ProjectFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': True}),
        }


class ModificationForm(forms.ModelForm):
    class Meta:
        model = Modification
        fields = ['mod_type', 'mod_num', 'mod_desc', 'mod_amount',
                  'mod_approved', 'mod_executed', 'mod_notes']


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name']
