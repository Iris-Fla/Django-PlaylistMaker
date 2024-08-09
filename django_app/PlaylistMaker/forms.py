from django import forms
from .models import video_info

class VideoSelectionForm(forms.ModelForm):
    class Meta:
        model = video_info
        fields = ['is_selected']