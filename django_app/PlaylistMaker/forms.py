from django import forms
from .models import video_info

class VideoSelectionForm(forms.ModelForm):
    class Meta:
        model = video_info
        fields = ['is_selected']

# class FindForms(forms.Form):
#     find = forms.CharField(label='Find',required=False,\
#                            widget=forms.TextInput(attrs={'class':'form-control'}))
    

class SearchForm(forms.Form):
        keyword = forms.CharField(label='', max_length=50)