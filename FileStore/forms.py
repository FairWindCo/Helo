from dal import autocomplete
from django.forms import ModelForm, ModelChoiceField

from FileStore.models import Tag, Project


class ProjectForm(ModelForm):
    tags = ModelChoiceField(
        queryset=Tag.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='autocomlete_tags')
    )
    class Meta:
        model = Project
        fields = ('__all__')
        widgets = {
            'tags': autocomplete.ModelSelect2Multiple(url='autocomlete_tags',
                                                      attrs={
                                                          # Set some placeholder
                                                          'data-placeholder': 'Autocomplete ...',
                                                          # Only trigger autocompletion after 3 characters have been typed
                                                          'data-minimum-input-length': 3,
                                                      },
                                                      )
        }
