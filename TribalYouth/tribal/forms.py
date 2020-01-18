from django import forms
from .models import TribalSkills

class Skill_Form(forms.ModelForm):
    class Meta:
        model=TribalSkills
        fields = [
            'img','title','desc','email'
        ]