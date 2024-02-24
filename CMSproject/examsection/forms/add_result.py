#forms.py
from django import forms 

class FilterForm(forms.Form):
    faculty_choices = [
        ('Computer', 'computer'),
        ('Civil', 'civil'),
        ('Architecture', 'architecture'),
        ('Electrical', 'electrical'),
        ('Electronics', 'electronics'),
    ]
    semester_choices = [(str(i), str(i)) for i in range(1, 9)]
    exam_type_choices = [('Regular', 'regular'), ('Back', 'back')]

    faculty = forms.ChoiceField(choices=faculty_choices, required=True)
    semester = forms.ChoiceField(choices=semester_choices, required=True)
    exam_type = forms.ChoiceField(choices=exam_type_choices, required=False)
    batch_number = forms.IntegerField(min_value=1998, required=True)

    def get_filter_metadata(self):
        # Return a dictionary containing the import metadata
        return {
            'faculty': self.cleaned_data['faculty'],
            'semester': self.cleaned_data['semester'],
            'exam_type': self.cleaned_data['exam_type'],
            'batch_number': self.cleaned_data['batch_number'],
        }

        
