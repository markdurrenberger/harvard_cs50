from django.shortcuts import render
from django.http import HttpResponse
from django import forms

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "searchbar": SearchBar()

    })

def page(request, title):
 
    ### Change this so all are made lower, so capitalization doesn't throw it off 
    if title.lower() in [x.lower() for x in util.list_entries()]:
        return render(request, "encyclopedia/page.html", {
            "page":util.get_entry(title), "title": title,
            "searchbar": SearchBar()
        })      
    else:
        return render(request, "encyclopedia/error.html")

### There has to be a better way to include this search on the layout.html without passing the context
### for every single other view
class SearchBar(forms.Form):
    # From online forum answer, how to include placeholder text
    ### Look more into the widgets part of forms
    search = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

def search(request):
    ### This will take in a string "search" and then see if that exists in current entries
    # Check if request method is post (i.e. if the form's method is post, which ours is)
    if request.method == "POST":
        # Take in the user data from submitted form
        form = SearchBar(request.POST)
        # Check if valid
        if form.is_valid():
            search = form.cleaned_data["search"]

            # if the search results are an entry, return that page
            if search.lower() in [x.lower() for x in util.list_entries()]:
                return render(request, "encyclopedia/page.html", {
                    "page":util.get_entry(search), "title":search,
                    "searchbar": SearchBar()
                })

            # If the search results are NOT an entry
            else:
                # I need to find all the entries in which search is a substring of the entry
                # then render the search page with that list as the value of a "results" key
                results = []

                for entry in [x.lower() for x in util.list_entries()]:
                    if search.lower() in entry:
                        results.append(entry)

                return render(request, "encyclopedia/search.html", {
                    "searchbar": SearchBar(), "results": results
                })


        

def new(request):
    #For now just renders our blank new entry page
    return render(request, "encyclopedia/new.html", {
        "searchbar": SearchBar()
    })

def edit(request):
    # For now, just takes to a static "edit" page
    return render(request, "encyclopedia/edit.html", {
        "searchbar": SearchBar()
    })

def random(request):
    # Takes user to a random page from the current list of entries
    import random
    # Get a list of all the current entries
    entries = util.list_entries()

    # select a random one
    selection = random.choice(entries)

    # render the page view with that entry 
    return render(request, "encyclopedia/page.html", {
        "page":util.get_entry(selection), "title":selection, 
        "searchbar": SearchBar()
    })
        
