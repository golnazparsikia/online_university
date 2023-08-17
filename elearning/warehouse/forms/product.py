from django import forms
from django.core.exceptions import ValidationError

from ..models import Division
from ..helper.consts import Scope


class DivisionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DivisionForm, self).__init__(*args, **kwargs)
        self.fields['scope'].initial = Scope.DIVISION
        self.fields['scope'].widget = forms.HiddenInput()

    class Meta:
        model = Division
        fields = tuple()

    def clean_scope(self):
        scope = self.cleaned_data['scope']
        if scope != Scope.DIVISION:
            raise ValidationError('Scope must be Division.')
        return scope
