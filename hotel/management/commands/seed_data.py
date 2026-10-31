from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from hotel.models import Amenite, Hotel, Review, Room

AMENITIES = [
    ("Wi-Fi", "Безкоштовний швидкісний інтернет у всьому готелі."),
    ("Сніданок", "Шведський стіл щоранку з 7:30 до 10:30."),
    ("Парковка", "Безкоштовна охоронювана парковка для гостей."),
    ("Басейн", "Критий басейн із підігрівом, відкритий щодня."),
    ("СПА", "Сауна, хамам і масажні кабінети."),
    ("Ресторан", "Ресторан української та європейської кухні."),
    ("Кондиціонер", "Індивідуальне керування кліматом у кожному номері."),
    ("Тренажерний зал", "Сучасний зал, відкритий цілодобово."),
    ("Трансфер", "Трансфер із вокзалу чи аеропорту за попереднім замовленням."),
    ("Дозволено з тваринами", "Приймаємо гостей із домашніми улюбленцями."),
]

HOTELS = [
    {
        "name": "Львівська Оселя",
        "country": "Україна",
        "city": "Львів",
        "address": "вул. Руська, 12",
        "price_per_night": "2200.00",
        "description": (
            "Затишний бутик-готель у серці старого Львова, за п'ять хвилин пішки "
            "від площі Ринок. Автентичні цегляні стіни, дерев'яні балки та кава, "
            "яку подають у ліжко, якщо ви цього захочете."
        ),
        "amenities": ["Wi-Fi", "Сніданок", "Ресторан", "Кондиціонер"],
        "rooms": [
            ("101", "single", 1, "1500.00"),
            ("102", "double", 2, "2200.00"),
            ("201", "double", 3, "2600.00"),
            ("301", "suite", 4, "4200.00"),
        ],
        "reviews": [
            (Decimal("9.5"), "Неймовірна атмосфера і чудовий сніданок. Повернемося ще!"),
            (Decimal("8.8"), "Дуже зручне розташування, привітний персонал."),
        ],
    },
    {
        "name": "Київський Дворик",
        "country": "Україна",
        "city": "Київ",
        "address": "вул. Хрещатик, 25",
        "price_per_night": "3100.00",
        "description": (
            "Сучасний готель на головній вулиці столиці з видом на місто. "
            "Ідеальний для ділових поїздок і вікендів: поруч метро, театри та "
            "найкращі ресторани."
        ),
        "amenities": ["Wi-Fi", "Сніданок", "Тренажерний зал", "Парковка", "Кондиціонер", "Трансфер"],
        "rooms": [
            ("101", "single", 1, "2000.00"),
            ("202", "double", 2, "3100.00"),
            ("203", "double", 3, "3500.00"),
            ("501", "suite", 4, "6000.00"),
        ],
        "reviews": [
            (Decimal("9.0"), "Чисто, тихо, зручний номер для роботи. Сніданки смачні."),
            (Decimal("8.5"), "Хороший сервіс і вигідна локація."),
        ],
    },
    {
        "name": "Одеський Бриз",
        "country": "Україна",
        "city": "Одеса",
        "address": "Французький бульвар, 40",
        "price_per_night": "2800.00",
        "description": (
            "Курортний готель за кілька кроків від моря з власним басейном і "
            "терасою. Прокидайтеся під шум хвиль і снідайте з видом на узбережжя."
        ),
        "amenities": ["Wi-Fi", "Басейн", "Сніданок", "Парковка", "Ресторан", "Дозволено з тваринами"],
        "rooms": [
            ("101", "single", 1, "1800.00"),
            ("102", "double", 2, "2800.00"),
            ("201", "double", 3, "3200.00"),
            ("301", "suite", 4, "5200.00"),
        ],
        "reviews": [
            (Decimal("9.2"), "Чудовий басейн, до моря кілька хвилин пішки. Відпочили на відмінно."),
            (Decimal("8.7"), "Привітний персонал, смачна кухня, з нами були з собакою, і проблем не було."),
        ],
    },
    {
        "name": "Карпатська Мрія",
        "country": "Україна",
        "city": "Буковель",
        "address": "вул. Курортна, 7",
        "price_per_night": "3500.00",
        "description": (
            "Гірський готель біля підйомників із видом на Карпати. Після катання "
            "на лижах чекають СПА, сауна та вогнище на терасі."
        ),
        "amenities": ["Wi-Fi", "СПА", "Сніданок", "Ресторан", "Парковка", "Трансфер"],
        "rooms": [
            ("101", "single", 1, "2400.00"),
            ("102", "double", 2, "3500.00"),
            ("201", "double", 3, "3900.00"),
            ("301", "suite", 4, "6500.00"),
        ],
        "reviews": [
            (Decimal("9.8"), "Найкращий відпочинок у горах! СПА після лиж просто розкіш."),
            (Decimal("9.1"), "Мальовничі краєвиди, затишні номери, дуже смачний ресторан."),
        ],
    },
]


class Command(BaseCommand):
    help = "Заповнює базу тестовими готелями, номерами, зручностями та відгуками."

    @transaction.atomic
    def handle(self, *args, **options):
        amenities = {}
        for name, description in AMENITIES:
            obj, _ = Amenite.objects.get_or_create(
                name=name, defaults={"description": description}
            )
            amenities[name] = obj

        for data in HOTELS:
            hotel, created = Hotel.objects.get_or_create(
                name=data["name"],
                defaults={
                    "description": data["description"],
                    "price_per_night": Decimal(data["price_per_night"]),
                    "country": data["country"],
                    "city": data["city"],
                    "address": data["address"],
                },
            )
            hotel.amenities.set([amenities[n] for n in data["amenities"]])

            for number, room_type, capacity, price in data["rooms"]:
                Room.objects.get_or_create(
                    hotel=hotel,
                    room_number=number,
                    defaults={
                        "room_type": room_type,
                        "capacity": capacity,
                        "price_per_night": Decimal(price),
                        "is_available": True,
                    },
                )

            if created:
                for rating, comment in data["reviews"]:
                    Review.objects.create(hotel=hotel, rating=rating, comment=comment)

            state = "створено" if created else "уже існує"
            self.stdout.write(self.style.SUCCESS(f"{hotel.name}: {state}"))

        self.stdout.write(self.style.SUCCESS("Готово!"))