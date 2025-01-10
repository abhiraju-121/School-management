from django import forms
from .models import Course,Subject

class CourseForm(forms.ModelForm):
    class Meta:
        model= Course
        fields =['name','description']

class SubjectForm(forms.ModelForm):
    class Meta:
        model= Subject
        fields =['course','sub_name']