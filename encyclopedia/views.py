from django.shortcuts import render, redirect
from encyclopedia.util import get_entry
from markdown2 import Markdown
import random

from . import util
    

def index(request):
    query = request.GET.get('q',)
    if query:
        # using 'list comprehensions' to lowercase the list. https://stackoverflow.com/questions/1801668/convert-a-list-with-strings-all-to-lowercase-or-uppercase
        if query.lower() in [e.lower() for e in util.list_entries()]:
            return redirect('title', title=query)
        elif query:
            entries_list = util.list_entries()
            filtered_list = []
            for entry in entries_list:
                if query.lower() in entry.lower():
                    filtered_list.append(entry)
            return render (request, "encyclopedia/index.html", {
            "entries": filtered_list
            })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

def title(request, title):
    wiki = get_entry(title)
    if wiki:
        markdowner = Markdown()
        return render(request, "encyclopedia/title.html", {
        "wiki_text": markdowner.convert(wiki),
        "title":title
        })
    else:
        return render(request, "encyclopedia/title.html", {
        "wiki_text": "<h1>Requested page was not found</h1>",
        "title":"Not Found"
        })
    
def new_page(request):
    if request.method =="POST":
        title_form = request.POST.get('title_form')
        text_form = request.POST.get('text_form')
        if title_form.lower() not in [e.lower() for e in util.list_entries()]:
            with open(f"entries/{title_form}.md", "x",encoding="utf-8") as f:
                f.write(text_form)
            return redirect('title', title=title_form)
        else:
            return render(request, "encyclopedia/new_page.html",{
                "info":"File name exist."
            })
    else:
        return render(request, "encyclopedia/new_page.html")
    
def edit_page(request,title):
    if request.method =="POST":
        text_form = request.POST.get('text_form')
        with open(f"entries/{title}.md", "w",encoding="utf-8") as f:
                f.write(text_form)
        return redirect('title', title=title)
    else:
        with open(f"entries/{title}.md", "r") as file:
            content = file.read()
        return render(request, "encyclopedia/edit_page.html",{
            "content":content,
            "title":title
        })
    
def random_page(request):
    entries = util.list_entries()
    # random function https://www.w3schools.com/python/ref_random_choice.asp
    r = random.choice(entries)
    return redirect('title', title=r)