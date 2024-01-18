from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializer import *


@api_view(["GET"])
def search_thematics(request):

    query = request.GET.get("query")

    thematics = Thematic.objects.filter(status=1).filter(name__icontains=query)

    serializer = ThematicSerializer(thematics, many=True)

    data = {
        "thematics": serializer.data
    }

    return Response(data)


@api_view(["GET"])
def get_thematic_by_id(request, thematic_id):
    if not Thematic.objects.filter(pk=thematic_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    thematic = Thematic.objects.get(pk=thematic_id)
    serializer = ThematicSerializer(thematic, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_thematic(request, thematic_id):
    if not Thematic.objects.filter(pk=thematic_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    thematic = Thematic.objects.get(pk=thematic_id)
    serializer = ThematicSerializer(thematic, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
def create_thematic(request):
    Thematic.objects.create()

    thematics = Thematic.objects.all()
    serializer = ThematicSerializer(thematics, many=True)
    
    return Response(serializer.data)


@api_view(["DELETE"])
def delete_thematic(request, thematic_id):
    if not Thematic.objects.filter(pk=thematic_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    thematic = Thematic.objects.get(pk=thematic_id)
    thematic.status = 2
    thematic.save()

    thematics = Thematic.objects.filter(status=1)
    serializer = ThematicSerializer(thematics, many=True)
    
    return Response(serializer.data)


@api_view(["POST"])
def add_thematic_to_exhibition(request, thematic_id):
    if not Thematic.objects.filter(pk=thematic_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    thematic = Thematic.objects.get(pk=thematic_id)

    exhibition = Exhibition.objects.filter(status=1).last()

    if exhibition is None:
        exhibition = Exhibition.objects.create()

    exhibition.thematics.add(thematic)
    exhibition.save()

    serializer = ThematicSerializer(exhibition.thematics, many=True)
    
    return Response(serializer.data)


@api_view(["GET"])
def get_thematic_image(request, thematic_id):
    if not Thematic.objects.filter(pk=thematic_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    thematic = Thematic.objects.get(pk=thematic_id)

    return HttpResponse(thematic.image, content_type="image/png")


@api_view(["PUT"])
def update_thematic_image(request, thematic_id):
    if not Thematic.objects.filter(pk=thematic_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    thematic = Thematic.objects.get(pk=thematic_id)
    serializer = ThematicSerializer(thematic, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)



@api_view(["GET"])
def get_exhibitions(request):
    exhibitions = Exhibition.objects.all()
    serializer = ExhibitionSerializer(exhibitions, many=True)
    
    return Response(serializer.data)


@api_view(["GET"])
def get_exhibition_by_id(request, exhibition_id):
    if not Exhibition.objects.filter(pk=exhibition_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    exhibition = Exhibition.objects.get(pk=exhibition_id)
    serializer = ExhibitionSerializer(exhibition, many=False)
    
    return Response(serializer.data)


@api_view(["PUT"])
def update_exhibition(request, exhibition_id):
    if not Exhibition.objects.filter(pk=exhibition_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    exhibition = Exhibition.objects.get(pk=exhibition_id)
    serializer = ExhibitionSerializer(exhibition, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    exhibition.status = 1
    exhibition.save()

    return Response(serializer.data)


@api_view(["PUT"])
def update_status_user(request, exhibition_id):
    if not Exhibition.objects.filter(pk=exhibition_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = request.data["status"]

    if request_status not in [1, 5]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    exhibition = Exhibition.objects.get(pk=exhibition_id)
    lesson_status = exhibition.status

    if lesson_status == 5:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    exhibition.status = request_status
    exhibition.save()

    serializer = ExhibitionSerializer(exhibition, many=False)
    
    return Response(serializer.data)


@api_view(["PUT"])
def update_status_admin(request, exhibition_id):
    if not Exhibition.objects.filter(pk=exhibition_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = request.data["status"]

    if request_status in [1, 5]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    exhibition = Exhibition.objects.get(pk=exhibition_id)

    lesson_status = exhibition.status

    if lesson_status in [3, 4, 5]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    exhibition.status = request_status
    exhibition.save()

    serializer = ExhibitionSerializer(exhibition, many=False)
    
    return Response(serializer.data)


@api_view(["DELETE"])
def delete_exhibition(request, exhibition_id):
    if not Exhibition.objects.filter(pk=exhibition_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    exhibition = Exhibition.objects.get(pk=exhibition_id)
    exhibition.status = 5
    exhibition.save()
    
    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
def delete_thematic_from_exhibition(request, exhibition_id, thematic_id):
    if not Exhibition.objects.filter(pk=exhibition_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not Thematic.objects.filter(pk=thematic_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    exhibition = Exhibition.objects.get(pk=exhibition_id)
    exhibition.thematics.remove(Thematic.objects.get(pk=thematic_id))
    exhibition.save()

    serializer = ThematicSerializer(exhibition.thematics, many=True)
    
    return Response(serializer.data)

