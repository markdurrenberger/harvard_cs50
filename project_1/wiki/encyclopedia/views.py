from django.shortcuts import render
from django.http import HttpResponse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, title):
 
    ### Change this so all are made lower, so capitalization doesn't throw it off 
    if title.lower() in [x.lower() for x in util.list_entries()]:
        return render(request, "encyclopedia/page.html", {
            "page":util.get_entry(title), "title": title
        })      
    else:
        return render(request, "encyclopedia/error.html")
        
