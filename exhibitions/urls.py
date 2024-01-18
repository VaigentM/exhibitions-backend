from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name="home"),
    path('thematics/<int:thematic_id>', thematic_details, name="thematic_details"),
    path('thematics/<int:thematic_id>/delete/', thematic_delete, name="thematic_delete")
]
