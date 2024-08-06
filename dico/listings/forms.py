# forms.py
from django import forms
from .models import Word, Category, Dictionary

#formulaire de création du dictionnaire
class DictionaryForm(forms.ModelForm):
 
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Dictionary.objects.filter(name=name).exists():
            raise forms.ValidationError("Un dictionnaire avec ce nom existe déjà.")
        return name
    class Meta:
        model = Dictionary
        fields = ['name'] 

#formulaire de création du champs de recherche de mots
class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label="Recherche")

#formulaire de création du formulaire d'ajout de nouveaux mots
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

        # Définir la catégorie par défaut "no category"
        default_category, created = Category.objects.get_or_create(name="no category")
        self.fields["category"].initial = default_category

    def clean(self):
        cleaned_data = super().clean()
        new_category = cleaned_data.get("new_category")
        category = cleaned_data.get("category")

        if not new_category and not category:
            # Si aucune catégorie n'est choisie ou créée, définir la catégorie par défaut
            default_category, created = Category.objects.get_or_create(name="no category")
            cleaned_data["category"] = default_category

        return cleaned_data

    def save(self, commit=True):
        new_category = self.cleaned_data.get("new_category")
        if new_category:
            category, created = Category.objects.get_or_create(name=new_category)
            self.instance.category = category
        return super().save(commit)