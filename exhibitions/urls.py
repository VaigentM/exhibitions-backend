from django.urls import path
from .views import *

urlpatterns = [
    # Набор методов для услуг
    path('api/thematics/search', search_thematics),  # GET
    path('api/thematics/<int:thematic_id>/', get_thematic_by_id),  # GET
    path('api/thematics/<int:thematic_id>/update/', update_thematic),  # PUT
    path('api/thematics/<int:thematic_id>/delete/', delete_thematic),  # DELETE
    path('api/thematics/create/', create_thematic),  # POST
    path('api/thematics/<int:thematic_id>/add_to_exhibition/', add_thematic_to_exhibition),  # POST
    path('api/thematics/<int:thematic_id>/image/', get_thematic_image),  # GET
    path('api/thematics/<int:thematic_id>/update_image/', update_thematic_image),  # PUT

    # Набор методов для заявок
    path('api/exhibitions/', get_exhibitions),  # GET
    path('api/exhibitions/<int:exhibition_id>/', get_exhibition_by_id),  # GET
    path('api/exhibitions/<int:exhibition_id>/update/', update_exhibition),  # PUT
    path('api/exhibitions/<int:exhibition_id>/update_status_user/', update_status_user),  # PUT
    path('api/exhibitions/<int:exhibition_id>/update_status_admin/', update_status_admin),  # PUT
    path('api/exhibitions/<int:exhibition_id>/delete/', delete_exhibition),  # DELETE
    path('api/exhibitions/<int:exhibition_id>/delete_thematic/<int:thematic_id>/', delete_thematic_from_exhibition),  # DELETE
]
