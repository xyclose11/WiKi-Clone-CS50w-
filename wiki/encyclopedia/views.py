from hmac import new
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django import forms
import markdown
import random

from . import util
import encyclopedia


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def display(request, entryName):

    if util.get_entry(entryName) != None:
        return render(request, "encyclopedia/display.html", {
            "entry": markdown.markdown(util.get_entry(entryName), output_format="html"),
            "entryName":entryName
        })
    else:
        return render(request, "encyclopedia/error.html")
    
def search(request):

    if request.method == "POST":
        test = request.POST
        
        if util.get_entry(test.get("q")) is not None:
            return render(request, "encyclopedia/display.html", {
                "entry": markdown.markdown(util.get_entry(test.get("q")), output_format="html")
        })
        else:
            searchList = []
            for i in util.list_entries():
                if test.get("q") in i.lower():
                    searchList.append(i)

            return render(request, "encyclopedia/display.html", {
                "entriesSearch": searchList
        })

def newentry(request):

    if request.method == "POST":
        newEntryData = request.POST

        newTitle = newEntryData.get("title")

        if newTitle in util.list_entries():
            return render(request, "encyclopedia/duplicateError.html")
        
        else:
            util.save_entry(newTitle, newEntryData.get("newEntryBody"))
            return render(request, "encyclopedia/display.html", {
                "entry": markdown.markdown(util.get_entry(newTitle), output_format="html")
            })

    else:
        return render(request, "encyclopedia/newEntry.html")
    
class EditEntryForm(forms.Form):
    EntryTitle = forms.CharField(label="Title")
    EntryBody = forms.CharField(label="Entry Body")
    
def edit(request):
    if request.method == "POST":
        editEntryData = request.POST

        form = EditEntryForm(request.POST)

        #if form.is_valid():
            #editTitle = form.cleaned_data['EntryTitle']

        editTitle = editEntryData.get("entryTitle")

        return render(request, "encyclopedia/edit.html", {
            "entryTitle":editTitle,
            "entryBody":util.get_entry(editTitle),
            #"EntryTitle": EditEntryForm(),
            #"EntryBody": EditEntryForm(),
        })

def save(request):
    if request.method == "POST":
        saveEntryData = request.POST

        saveTitle = saveEntryData.get("saveTitle")
        saveBody = saveEntryData.get("editEntryBody")

        util.save_entry(saveTitle, bytes(saveBody, 'utf8'))
        return HttpResponseRedirect(reverse("encyclopedia:display", args=[saveTitle]))
    
def randomentry(request):
    ListedEntries = util.list_entries()
    EntryCount = len(ListedEntries)
    rand = random.randrange(EntryCount)
    return HttpResponseRedirect(reverse("encyclopedia:display", args=[ListedEntries[int(rand)]]))


        
