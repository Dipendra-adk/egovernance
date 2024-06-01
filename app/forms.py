from django import forms
from .models import Tender

class TenderForm(forms.ModelForm):
    class Meta:
        model = Tender
        fields = ['category', 'title', 'description', 'deadline', 'baseprice', 'contractor_company_name', 'contractor_name', 'contractor_email', 'contractor_phone', 'planning_phase1_date', 'planning_phase1_payment', 'planning_phase2_date', 'planning_phase2_payment', 'planning_final_date', 'planning_final_payment', 'terms_and_conditions', 'status', 'winner']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'planning_phase1_date': forms.DateInput(attrs={'type': 'date'}),
            'planning_phase2_date': forms.DateInput(attrs={'type': 'date'}),
            'planning_final_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
    # Override the __init__ method to customize the deadline field
    def __init__(self, *args, **kwargs):
        super(TenderForm, self).__init__(*args, **kwargs)
        # Set the input type for the deadline field to datetime-local
        self.fields['deadline'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')
     
        # Override the clean_image method to handle image validation
    def clean_image(self):
        image = self.cleaned_data.get('image')
        # Ensure that the uploaded file is an image
        if image:
            if not image.content_type.startswith('image'):
                raise forms.ValidationError("Uploaded file is not an image.")
        return image
    
# class BidderForm(forms.ModelForm):
#     class Meta:
#         model = Bidder
#         fields = ['company_name', 'email', 'phone', 'address']    