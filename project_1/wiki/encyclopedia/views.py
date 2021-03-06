from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
# Manybe can delete this one and HTTPredirect if the below one works
from django.urls import reverse
from django.shortcuts import redirect

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "searchbar": SearchBar()

    })

def page(request, title):
    
    # For when we are sent to the content page of a new entry from views.new
    if request.method == "POST":
        form = NewEntryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            # If the entry already exists, send to error page
            if title.lower() in [x.lower() for x in util.list_entries()]:
                return render(request, "encyclopedia/error-existing-entry.html",{
                    "searchbar": SearchBar()
                })

            # Otherwise, save that entry and then redirect to that page
            else:
                # Use existing util function to save the entry
                util.save_entry(title, content)

                return redirect(f'http://127.0.0.1:8000/{title}')

    # If it's just a normal "GET" request, run this and return the page (or error)
    if title.lower() in [x.lower() for x in util.list_entries()]:
        return render(request, "encyclopedia/page.html", {
            "content":util.get_entry(title), "title": title,
            "searchbar": SearchBar()
        })      
    else:
        return render(request, "encyclopedia/error.html", {
            "searchbar":SearchBar()
        })


### There has to be a better way to include this search on the layout.html without passing the context
### for every single other view
    ###There is something called a context manager that can be used, but that seems a bit complicated
    ### for right now. Come back and refactor this part as you continue the course.
class SearchBar(forms.Form):
    # From online forum answer, how to include placeholder text
    ### Look more into the widgets part of forms
    search = forms.CharField(label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Search Encyclopedia', 'size':15}))

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
                return redirect(f'http://127.0.0.1:8000/{search}')

            # If the search results are NOT an entry
            else:
                # I need to find all the entries in which search is a substring of the entry
                # then render the search page with that list as the value of a "results" key
                results = []

                for entry in util.list_entries():
                    if search.lower() in entry.lower():
                        results.append(entry)

                return render(request, "encyclopedia/search.html", {
                    "searchbar": SearchBar(), "results": results
                })


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder':'Enter entry content in markdown...', 'rows':5, 'cols':20
    }))

def new(request):
    # Takes user to new entry page - with a blank form ready to go
    return render(request, "encyclopedia/new.html", {
        "searchbar": SearchBar(), "newentry": NewEntryForm()
    })

class EditEntryForm(forms.Form):
    # Need to somehow keep the title/entry name from the page
        ## Figured this out: I pass that through the edit() view but assigning initial value!    
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea)

def edit(request):
    if request.method == "POST":
        # access the request's title
        title = request.POST['title']
        content = str(util.get_entry(title))

        return render(request, "encyclopedia/edit.html", {
            "title":title, "searchbar": SearchBar(), "editentry":EditEntryForm(initial={
                "content":content, "title":title}), "content":content
        })

def confirm(request):
    if request.method == "POST":
        form = EditEntryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            util.save_entry(title, content)

            return redirect(f'http://127.0.0.1:8000/{title}')
    
    return render(request, "encyclopedia/confirm.html",)   

def random(request):
    # Takes user to a random page from the current list of entries
    import random
    # Get a list of all the current entries
    entries = util.list_entries()

    # select a random one
    selection = random.choice(entries)

    # redirect them to the page for the randomly selected item
    return redirect(f'http://127.0.0.1:8000/{selection}')
   
        
