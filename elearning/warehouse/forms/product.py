from django import forms
from django.core.exceptions import ValidationError

from ..models import (
    Division,
    Bootcamp,
    Course,
    Lesson,
    Chapter,
    Project,
    Practice
)
from ..helper.consts import Scope

class DivisionForm(forms.ModelForm) :
    """
    Custom form for creating/editing Division instances.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['scope'].initial = Scope.DIVISION
    
    class Meta:
        model = Division
        fields = ('__all__')
        
    def clean_scope(self):
        scope = self.cleaned_data['scope']
        if scope != Scope.DIVISION:
            raise ValidationError('Scope must be Division.')
        return scope

class BootcampForm(forms.ModelForm) :
    """
    Custom form for creating/editing Bootcamp instances.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['scope'].initial = Scope.BOOTCAMP
    
    class Meta:
        model = Bootcamp
        fields = ('__all__')
        
    def clean_scope(self):
        scope = self.cleaned_data['scope']
        if scope != Scope.BOOTCAMP:
            raise ValidationError('Scope must be Bootcamp.')
        return scope

class CourseForm(forms.ModelForm) :
    """
    Custom form for creating/editing Course instances.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['scope'].initial = Scope.COURSE
    
    class Meta:
        model = Course
        fields = ('__all__')
        
    def clean_scope(self):
        scope = self.cleaned_data['scope']
        if scope != Scope.COURSE:
            raise ValidationError('Scope must be Course.')
        return scope

class LessonForm(forms.ModelForm) :
    """
    Custom form for creating/editing Lesson instances.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['scope'].initial = Scope.LESSON
    
    class Meta:
        model = Lesson
        fields = ('__all__')
        
    def clean_scope(self):
        scope = self.cleaned_data['scope']
        if scope != Scope.LESSON:
            raise ValidationError('Scope must be Lesson.')
        return scope

class ChapterForm(forms.ModelForm) :
    """
    Custom form for creating/editing Chapter instances.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['scope'].initial = Scope.CHAPTER
    
    class Meta:
        model = Chapter
        fields = ('__all__')
        
    def clean_scope(self):
        scope = self.cleaned_data['scope']
        if scope != Scope.CHAPTER:
            raise ValidationError('Scope must be Chapter.')
        return scope

class ProjectForm(forms.ModelForm) :
    """
    Custom form for creating/editing Project instances.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['scope'].initial = Scope.PROJECT
    
    class Meta:
        model = Project
        fields = ('__all__')
        
    def clean_scope(self):
        scope = self.cleaned_data['scope']
        if scope != Scope.PROJECT:
            raise ValidationError('Scope must be Project.')
        return scope

class PracticeForm(forms.ModelForm) :
    """
    Custom form for creating/editing Practice instances.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['scope'].initial = Scope.PRACTICE
    
    class Meta:
        model = Practice
        fields = ('__all__')
        
    def clean_scope(self):
        scope = self.cleaned_data['scope']
        if scope != Scope.PRACTICE:
            raise ValidationError('Scope must be Practice.')
        return scope
