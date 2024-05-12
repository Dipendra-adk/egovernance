from django import forms
from .models import Tender

class TenderForm(forms.ModelForm):
    class Meta:
        model = Tender
        fields = ['category', 'title', 'image', 'description', 'deadline', 'baseprice', 'owner', 'status', 'winner']
        
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