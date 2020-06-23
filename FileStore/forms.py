from dal import autocomplete
from django.forms import ModelForm, ModelChoiceField, ModelMultipleChoiceField

from FileStore.models import Tag, Project


class ProjectForm(ModelForm):
    # tags = ModelMultipleChoiceField(
    #     queryset=Tag.objects.all(),
    #     #widget=autocomplete.ModelSelect2Multiple(url='autocomlete_tags')
    # )
    class Meta:
        model = Project
        fields = ('name', 'comments', 'tags')
        widgets = {
            'tags': autocomplete.ModelSelect2Multiple(url='auto_tags',
                                                      attrs={
                                                          # Set some placeholder
                                                          'data-placeholder': 'Наберите начало тега ...',
                                                          # Only trigger autocompletion after 3 characters have been typed
                                                          'data-minimum-input-length': 3,
                                                          'title': 'Теги'
                                                      },
                                                      )
        }
