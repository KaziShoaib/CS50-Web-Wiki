from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import markdown2
import random
from . import util


def entryExists(query):
    entryNames = util.list_entries()
    return query.lower() in (entryName.lower() for entryName in entryNames)


def index(request):
    if request.method == "POST":
        query = request.POST['q']
        if entryExists(query):
            return HttpResponseRedirect(reverse("entry", args=[query]))
        else:
            return HttpResponseRedirect(reverse("search", args=[query]))

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })



def search(request, query):
    entryNames = util.list_entries()
    matches = [entryName for entryName in entryNames if query.lower() in entryName.lower()]
    return render(request, "encyclopedia/search.html", {
        "query" : query,
        "entries" : matches
    })


def create(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        if entryExists(title):
            return HttpResponseRedirect(reverse("conflict"))
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", args=[title]))

    return render(request, "encyclopedia/create.html")



def conflict(request):
    return render(request, "encyclopedia/conflict.html")



def edit(request, title):
    if request.method == "POST":
        content = request.POST['content']
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", args=[title]))

    mdContent = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "title" : title,
        "content" : mdContent
    })


def randompage(request):
    entryNames = util.list_entries()
    title = random.choice(entryNames)
    return HttpResponseRedirect(reverse("entry", args=[title]))


def entry(request, title):
    mdContent = util.get_entry(title)
    if mdContent is None:
        htmlContent = None
    else:
        htmlContent = markdown2.markdown(mdContent)
    return render(request, "encyclopedia/entry.html", {
        "title":title,
        "content":htmlContent
    })


