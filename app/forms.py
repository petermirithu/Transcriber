from django import forms
from app.models import audio_files

class UploadFileForm(forms.ModelForm):    
    class Meta:
        model=audio_files
        fields=['file_au']
