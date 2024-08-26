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
        keyword = forms.CharField(label='', max_length=50,required=False)

class FilterForm(forms.Form):
    ORDER_CHOICES = [
        ('published_date', '投稿日'),
        ('views', '再生回数'),
    ]
    DIRECTION_CHOICES = [
        ('asc', '昇順'),
        ('desc', '降順'),
    ]
    order_by = forms.ChoiceField(choices=ORDER_CHOICES, required=False)
    direction = forms.ChoiceField(choices=DIRECTION_CHOICES, required=False)
    min_views = forms.IntegerField(required=False, min_value=0)
    max_views = forms.IntegerField(required=False, min_value=0)
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))