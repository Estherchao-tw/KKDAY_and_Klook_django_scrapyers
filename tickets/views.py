from django.shortcuts import render
from django.template import loader
from .scrapers import Kkday

from django.http import HttpResponse

# def home(request):
#     return HttpResponse("Hello, Django!")

def index(request):


    kkday = Kkday(request.POST.get("city_name"))


    context = {
        "tickets" : kkday.scrape()
    }

    return render(request, "tickets/index.html",context)