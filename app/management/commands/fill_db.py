import random

from django.core import management
from django.core.management.base import BaseCommand
from app.models import *
from .utils import random_date, random_timedelta, random_text


def add_thematics():
    Thematic.objects.create(
        name="Робототехника",
        description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam mollis sagittis metus, non laoreet ipsum consectetur at.",
        image="thematics/1.png"
    )

    Thematic.objects.create(
        name="Аддитивное производство",
        description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam mollis sagittis metus, non laoreet ipsum consectetur at.",
        image="thematics/2.png"
    )

    Thematic.objects.create(
        name="Искусственный интеллект",
        description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam mollis sagittis metus, non laoreet ipsum consectetur at.",
        image="thematics/3.png"
    )

    Thematic.objects.create(
        name="Экология",
        description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam mollis sagittis metus, non laoreet ipsum consectetur at.",
        image="thematics/4.png"
    )

    Thematic.objects.create(
        name="Исскуственный интелект",
        description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam mollis sagittis metus, non laoreet ipsum consectetur at.",
        image="thematics/5.png"
    )


    print("Услуги добавлены")


def generate_room():
    number = random.randint(0, 831) + 200

    if number > 700:
        return f"{number}л"

    if number < 400 and random.randint(0, 10) < 3:
        return f"{number}э"

    return number


def add_exhibitions():
    owners = CustomUser.objects.filter(is_superuser=False)
    moderators = CustomUser.objects.filter(is_superuser=True)

    if len(owners) == 0 or len(moderators) == 0:
        print("Заявки не могут быть добавлены. Сначала добавьте пользователей с помощью команды add_users")
        return

    thematics = Thematic.objects.all()

    for _ in range(30):
        exhibition = Exhibition.objects.create()
        exhibition.name = random_text(4)
        exhibition.description = random_text(15)
        exhibition.status = random.randint(2, 5)
        exhibition.owner = random.choice(owners)

        if exhibition.status in [2, 3, 4]:
            exhibition.room = generate_room()

        if exhibition.status in [3, 4]:
            exhibition.date_complete = random_date()
            exhibition.date_formation = exhibition.date_complete - random_timedelta()
            exhibition.date_created = exhibition.date_formation - random_timedelta()
            exhibition.moderator = random.choice(moderators)
        else:
            exhibition.date_formation = random_date()
            exhibition.date_created = exhibition.date_formation - random_timedelta()


        for i in range(random.randint(1, 3)):
            exhibition.thematics.add(random.choice(thematics))

        exhibition.save()

    print("Заявки добавлены")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        management.call_command("clean_db")
        management.call_command("add_users")

        add_thematics()
        add_exhibitions()









