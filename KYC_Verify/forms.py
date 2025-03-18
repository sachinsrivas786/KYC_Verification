from django import forms


class CandidateForm(forms.Form):
    employee_id = forms.CharField(label="Employee ID", max_length=6, required=True,  widget=forms.NumberInput(attrs={'class': 'form-control','id':'emp_id','oninput': "if(this.value.length > 6) this.value = this.value.slice(0, 6)"}))
    password = forms.CharField(label="Enter Your Password", max_length=20,required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}, render_value=False))

    def clean_employee_id(self):
        employee_id = self.cleaned_data['employee_id']
        if len(employee_id) > 6:
            raise forms.ValidationError("Employee ID cannot be more than 6 digits.")
        return employee_id