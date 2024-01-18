from django.core.management.base import BaseCommand
from app.models import *


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Exhibition.objects.all().delete()
        Thematic.objects.all().delete()
        CustomUser.objects.all().delete()