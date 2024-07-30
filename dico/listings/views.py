# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Dictionary, Word
from listings.forms import NewWordForm, DictionaryForm


def home_page(request):
    return render(request, "listings/base.html")


def dictionary_list(request):
    dictionaries = Dictionary.objects.all()
    return render(
        request, "listings/dictionary_list.html", {"dictionaries": dictionaries}
    )

def dictionary_add(request):
    if request.method == 'POST':
        form = DictionaryForm(request.POST)
        if form.is_valid():
            # Créer un nouveau dictionnaire et le sauvegarder dans la DB
            form.save()
            # Rediriger vers la liste des dictionnaires
            return redirect('dictionary-list')
    else:
        form = DictionaryForm()

    return render(request, 'listings/dictionary_list_add.html', {'form': form})
def dictionary_list_delete(request, id):
    dictionary = Dictionary.objects.get(id=id)  # nécessaire pour GET et pour POST

    if request.method == "POST":
        # supprimer le groupe de la base de données
        dictionary.delete()
        # rediriger vers la liste des groupes
        return redirect("dictionary-list")

    # pas besoin de « else » ici. Si c'est une demande GET, continuez simplement

    return render(
        request, "listings/dictionary_list_delete.html", {"dictionary": dictionary}
    )


def dictionary_detail(request, dictionary_id):
    dictionary = get_object_or_404(Dictionary, id=dictionary_id)
    words = Word.objects.filter(dictionary=dictionary)
    context = {
        "dictionary": dictionary,
        "words": words,
    }
    return render(request, "listings/words_list.html", context)


def new_word(request):
    if request.method == "POST":
        form = NewWordForm(request.POST)
        if form.is_valid():
            word = form.save()
            return redirect("dictionary-detail", dictionary_id=word.dictionary.id)
    else:
        form = NewWordForm()

    return render(request, "listings/new_word.html", {"form": form})
