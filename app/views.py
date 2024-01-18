import requests
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.utils.dateparse import parse_datetime
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .jwt_helper import *
from .permissions import *
from .serializers import *
from .utils import identity_user


def get_draft_exhibition(request):
    user = identity_user(request)

    if user is None:
        return None

    exhibition = Exhibition.objects.filter(owner_id=user.id).filter(status=1).first()

    return exhibition


@api_view(["GET"])
def search_thematics(request):
    query = request.GET.get("query", "")

    thematic = Thematic.objects.filter(status=1).filter(name__icontains=query)

    serializer = ThematicSerializer(thematic, many=True)

    draft_exhibition = get_draft_exhibition(request)

    resp = {
        "thematics": serializer.data,
        "draft_exhibition_id": draft_exhibition.pk if draft_exhibition else None
    }

    return Response(resp)


@api_view(["GET"])
def get_thematic_by_id(request, thematic_id):
    if not Thematic.objects.filter(pk=thematic_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    thematic = Thematic.objects.get(pk=thematic_id)
    serializer = ThematicSerializer(thematic)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_thematic(request, thematic_id):
    if not Thematic.objects.filter(pk=thematic_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    thematic = Thematic.objects.get(pk=thematic_id)
    serializer = ThematicSerializer(thematic, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsModerator])
def create_thematic(request):
    thematic = Thematic.objects.create()

    serializer = ThematicSerializer(thematic)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_thematic(request, thematic_id):
    if not Thematic.objects.filter(pk=thematic_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    thematic = Thematic.objects.get(pk=thematic_id)
    thematic.status = 5
    thematic.save()

    thematic = Thematic.objects.filter(status=1)
    serializer = ThematicSerializer(thematic, many=True)

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_thematic_to_exhibition(request, thematic_id):
    if not Thematic.objects.filter(pk=thematic_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    thematic = Thematic.objects.get(pk=thematic_id)

    exhibition = get_draft_exhibition(request)

    if exhibition is None:
        exhibition = Exhibition.objects.create()
        exhibition.date_perform = timezone.now()

    if exhibition.thematics.contains(thematic):
        return Response(status=status.HTTP_409_CONFLICT)

    exhibition.thematics.add(thematic)
    exhibition.owner = identity_user(request)
    exhibition.save()

    serializer = ExhibitionSerializer(exhibition)
    return Response(serializer.data)


@api_view(["GET"])
def get_thematic_image(request, thematic_id):
    if not Thematic.objects.filter(pk=thematic_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    thematic = Thematic.objects.get(pk=thematic_id)

    return HttpResponse(thematic.image, content_type="image/png")


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_thematic_image(request, thematic_id):
    if not Thematic.objects.filter(pk=thematic_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    thematic = Thematic.objects.get(pk=thematic_id)
    serializer = ThematicSerializer(thematic, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_exhibitions(request):
    user = identity_user(request)

    status_id = int(request.GET.get("status", -1))
    date_start = request.GET.get("date_start")
    date_end = request.GET.get("date_end")

    exhibitions = Exhibition.objects.exclude(status__in=[1, 5])
        
    if not user.is_moderator:
        exhibitions = exhibitions.filter(owner=user)

    if status_id > 0:
        exhibitions = exhibitions.filter(status=status_id)

    if date_start:
        exhibitions = exhibitions.filter(date_formation__gte=parse_datetime(date_start))

    if date_end:
        exhibitions = exhibitions.filter(date_formation__lte=parse_datetime(date_end))

    serializer = ExhibitionsSerializer(exhibitions, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_exhibition_by_id(request, exhibition_id):
    if not Exhibition.objects.filter(pk=exhibition_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    exhibition = Exhibition.objects.get(pk=exhibition_id)
    serializer = ExhibitionSerializer(exhibition)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_exhibition(request, exhibition_id):
    if not Exhibition.objects.filter(pk=exhibition_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    exhibition = Exhibition.objects.get(pk=exhibition_id)

    serializer = ExhibitionSerializer(exhibition, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    date_perform = request.data.get("date_perform")
    if date_perform:
        exhibition.date_estimate = parse_datetime(date_perform)

    exhibition.save()

    return Response(serializer.data)


@api_view(["PUT"])
def update_exhibition_room(request, exhibition_id):
    if not Exhibition.objects.filter(pk=exhibition_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    exhibition = Exhibition.objects.get(pk=exhibition_id)

    serializer = ExhibitionSerializer(exhibition, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_status_user(request, exhibition_id):
    if not Exhibition.objects.filter(pk=exhibition_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    exhibition = Exhibition.objects.get(pk=exhibition_id)

    exhibition.status = 2
    exhibition.date_formation = timezone.now()
    exhibition.save()

    calculate_room(exhibition_id)

    serializer = ExhibitionSerializer(exhibition)

    return Response(serializer.data)


def calculate_room(exhibition_id):
    data = {
        "exhibition_id": exhibition_id
    }

    requests.post("http://127.0.0.1:8080/calc_room/", json=data, timeout=3)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_status_admin(request, exhibition_id):
    if not Exhibition.objects.filter(pk=exhibition_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = int(request.data["status"])

    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    exhibition = Exhibition.objects.get(pk=exhibition_id)

    if exhibition.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    exhibition.moderator = identity_user(request)
    exhibition.status = request_status
    exhibition.date_complete = timezone.now()
    exhibition.save()

    serializer = ExhibitionSerializer(exhibition)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_exhibition(request, exhibition_id):
    if not Exhibition.objects.filter(pk=exhibition_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    exhibition = Exhibition.objects.get(pk=exhibition_id)

    if exhibition.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    exhibition.status = 5
    exhibition.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_thematic_from_exhibition(request, exhibition_id, thematic_id):
    if not Exhibition.objects.filter(pk=exhibition_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not Thematic.objects.filter(pk=thematic_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    exhibition = Exhibition.objects.get(pk=exhibition_id)
    exhibition.thematics.remove(Thematic.objects.get(pk=thematic_id))
    exhibition.save()

    if exhibition.thematics.count() == 0:
        exhibition.delete()
        return Response(status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_200_OK)


@swagger_auto_schema(method='post', request_body=UserLoginSerializer)
@api_view(["POST"])
def login(request):
    serializer = UserLoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(**serializer.data)
    if user is None:
        message = {"message": "invalid credentials"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token(user.id)

    user_data = {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "is_moderator": user.is_moderator,
        "access_token": access_token
    }

    response = Response(user_data, status=status.HTTP_201_CREATED)

    response.set_cookie('access_token', access_token, httponly=False, expires=settings.JWT["ACCESS_TOKEN_LIFETIME"])

    return response


@api_view(["POST"])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    user = serializer.save()

    access_token = create_access_token(user.id)

    message = {
        'message': 'User registered successfully',
        'user_id': user.id,
        "access_token": access_token
    }

    response = Response(message, status=status.HTTP_201_CREATED)

    response.set_cookie('access_token', access_token, httponly=False, expires=settings.JWT["ACCESS_TOKEN_LIFETIME"])

    return response


@api_view(["POST"])
def check(request):
    token = get_access_token(request)

    if token is None:
        message = {"message": "Token is not found"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    if token in cache:
        message = {"message": "Token in blacklist"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    payload = get_jwt_payload(token)
    user_id = payload["user_id"]

    user = CustomUser.objects.get(pk=user_id)
    serializer = UserSerializer(user)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    access_token = get_access_token(request)

    if access_token not in cache:
        cache.set(access_token, settings.JWT["ACCESS_TOKEN_LIFETIME"])

    message = {"message": "Вы успешно вышли из аккаунта"}
    response = Response(message, status=status.HTTP_200_OK)

    response.delete_cookie('access_token')

    return response
