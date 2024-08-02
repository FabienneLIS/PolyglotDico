# forms.py
from django import forms
from .models import Word, Category, Dictionary

class DictionaryForm(forms.ModelForm):
    class Meta:
        model = Dictionary
        fields = ['name'] 


class NewWordForm(forms.ModelForm):
    new_category = forms.CharField(
        max_length=100, required=False, label="Nouvelle catégorie"
    )

    class Meta:
        model = Word
        fields = ["source_word", "target_word", "category", "dictionary"]
        widgets = {
            'dictionary': forms.HiddenInput(),  # Masquer le champ dictionary
        }

    def __init__(self, *args, **kwargs):
        super(NewWordForm, self).__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.all()
        self.fields["category"].required = False  # Ne pas rendre ce champ obligatoire

    def clean(self):
        cleaned_data = super().clean()
        new_category = cleaned_data.get("new_category")
        category = cleaned_data.get("category")

        if not new_category and not category:
            raise forms.ValidationError(
                "Vous devez choisir une catégorie ou en créer une nouvelle."
            )

        return cleaned_data

    def save(self, commit=True):
        new_category = self.cleaned_data.get("new_category")
        if new_category:
            category, created = Category.objects.get_or_create(name=new_category)
            self.instance.category = category
        return super().save(commit)
