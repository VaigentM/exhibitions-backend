from django.shortcuts import render, redirect
from .models import *


def index(request):
    query = request.GET.get("query")
    thematics = Thematic.objects.filter(name__icontains=query).filter(status=1) if query else Thematic.objects.filter(status=1)

    context = {
        "search_query": query if query else "",
        "thematics": thematics
    }

    return render(request, "home_page.html", context)


def thematic_details(request, thematic_id):
    context = {
        "thematic": Thematic.objects.get(id=thematic_id)
    }

    return render(request, "thematic_page.html", context)


def thematic_delete(request, thematic_id):
    reactor = Thematic.objects.get(id=thematic_id)
    reactor.delete()

    return redirect("/")
