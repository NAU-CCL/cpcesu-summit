from django import forms

from .models import Project, File, Location, Modification, ModFile


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['award_office', 'budget', 'description', 'discipline', 'exec_start_date',
                  'federal_agency', 'field_of_science', 'final_report', 'fiscal_year', 'init_start_date', 'location',
                  'monitoring', 'notes', 'num_of_students', 'p_num', 'partner', 'pp_i', 'project_manager',
                  'project_title', 'r_d', 'reviewed', 'sci_method', 'sensitive', 'short_summary', 'src_of_funding',
                  'staff_member', 'status', 'tech_rep', 'tent_end_date', 'tent_start_date',
                  'task_agreement_start_date', 'type', 'field_of_science_sub', 'youth_vets']
        widgets = {
            'award_office': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'project_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title here...'}),
            'p_num': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter P-Num here...'}),
            'short_summary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Quick details...'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Abstract here...'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter any project notes here...'}),
            'status': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'partner': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'federal_agency': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'pp_i': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'project_manager': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'tech_rep': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'location': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control'}),
            'fiscal_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'youth_vets': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'cesu_unit': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'staff_member': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'discipline': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'r_d': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'src_of_funding': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'field_of_science': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'field_of_science_sub': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'type': forms.Select(attrs={'class': 'custom-select custom-select'}),
            'sensitive': forms.CheckboxInput(attrs={'class': 'custom-control custom-checkbox'}),
            'tent_start_date': forms.SelectDateWidget(years=list(range(1950, 3000)),
                                                      empty_label=("Year", "Month", "Day"),),
            'tent_end_date': forms.SelectDateWidget(years=list(range(1950, 3000)),
                                                      empty_label=("Year", "Month", "Day"),),
            'init_start_date': forms.SelectDateWidget(years=list(range(1950, 3000)),
                                                      empty_label=("Year", "Month", "Day"),),
            'exec_start_date': forms.SelectDateWidget(years=list(range(1950, 3000)),
                                                      empty_label=("Year", "Month", "Day"), ),
            'task_agreement_start_date': forms.SelectDateWidget(years=list(range(1950, 3000)),
                                                                empty_label=("Year", "Month", "Day"), ),
            'reviewed': forms.SelectDateWidget(years=list(range(1950, 3000)),
                                               empty_label=("Year", "Month", "Day"), ),

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
                  'mod_approved', 'mod_executed', 'mod_notes', 'mod_extension']
        widgets = {
            'mod_approved': forms.SelectDateWidget(years=list(range(1950, 3000)),
                                                   empty_label=("Year", "Month", "Day"), ),
            'mod_executed': forms.SelectDateWidget(years=list(range(1950, 3000)),
                                                   empty_label=("Year", "Month", "Day"), ),
            'mod_extension': forms.SelectDateWidget(years=list(range(1950, 3000)),
                                                    empty_label=("Year", "Month", "Day"), ),
        }


class ModificationFileForm(forms.ModelForm):
    class Meta:
        model = ModFile
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': True}),
        }


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name']


class ContactForm(forms.Form):
    your_name = forms.CharField(label="Your Name", max_length=100)
    your_email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    cc_myself = forms.BooleanField(required=False)
