# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Dictionary, Word, Category
from listings.forms import NewWordForm, DictionaryForm, SearchForm


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

def dictionary_update(request, id):
    dictionaries = Dictionary.objects.get(id=id)

    if request.method == 'POST':
        form = DictionaryForm(request.POST, instance=dictionaries)
        if form.is_valid():
            # mettre à jour le groupe existant dans la base de données
            form.save()
            # rediriger vers la page détaillée du groupe que nous venons de mettre à jour
            return redirect('band-detail', dictionaries.id)
    else:
        form = DictionaryForm(instance=dictionaries)

    return render(request,
                'listings/dictionary_list_update.html',
                {'form': form})

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
    search_form = SearchForm(request.GET or None)
    
    query = search_form.cleaned_data.get('query') if search_form.is_valid() else None
    if query:
        words = Word.objects.filter(
            dictionary=dictionary,
            source_word__icontains=query
        ) | Word.objects.filter(
            dictionary=dictionary,
            target_word__icontains=query
        )
    else:
        words = Word.objects.filter(dictionary=dictionary)
    
    context = {
        "dictionary": dictionary,
        "words": words,
        "search_form": search_form,
    }
    return render(request, "listings/words_list.html", context)


def new_word(request, dictionary_id):
    dictionary = get_object_or_404(Dictionary, id=dictionary_id)

    if request.method == "POST":
        form = NewWordForm(request.POST)
        if form.is_valid():
            word = form.save(commit=False)
            word.dictionary = dictionary
            if not word.category:
                default_category, created = Category.objects.get_or_create(name="no category")
                word.category = default_category
            word.save()
            return redirect("dictionary-detail", dictionary_id=dictionary.id)
    else:
        form = NewWordForm(initial={'dictionary': dictionary})

    categories = Category.objects.all()
    return render(request, "listings/new_word.html", {"form": form, "dictionary": dictionary, "categories": categories})



def new_word_delete(request, word_id):
    word = get_object_or_404(Word, id=word_id)

    if request.method == "POST":
        dictionary_id = word.dictionary.id  # Sauvegarder l'ID du dictionnaire pour redirection après suppression
        word.delete()
        return redirect("dictionary-detail", dictionary_id=dictionary_id)

    return render(
        request, "listings/word__delete.html", {"word": word}
    )