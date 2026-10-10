"""
Seeds the catalogue with the All Stars / EthioSolar product set.

    python manage.py seed_allstars

Idempotent: re-running updates existing rows instead of duplicating them.
"""

from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from catalog.models import Category, Product, ProductImage

CATEGORIES = [
    'Apparel',
    'Footwear',
    'Electronics',
    'Gear & Equipment',
    'Accessories',
    'Solar',
    'Audio Equipment',
    'Portable Solar Lighting Systems',
    'Advanced Solar Power & Generator Kits',
    'Solar Task & Desk Lighting',
]

# (name, category, price, short_description, description, main_image, gallery, is_featured)
PRODUCTS = [
    (
        'Foldable Solar Light', 'Solar', '1.00',
        'A compact, orange rechargeable utility light featuring a built-in solar panel, '
        'flexible wire stand for easy positioning, and bright LED illumination suitable for '
        'outdoor activities and emergency use. This device is assembled in Ethiopia.',
        'Experience pure audio fidelity with the Apex Pro Wireless Headphones. Featuring '
        'advanced hybrid active noise cancellation, custom 40mm titanium drivers, plush memory '
        'foam ear cushions, and crystal-clear microphone array for calls or streaming.',
        '/static/img/solar.jpg', ['/static/img/solar1.jpg'], True,
    ),
    (
        'Multi-Angle Solar light', 'Solar', '1.00',
        'A versatile portable lighting solution equipped with an integrated solar charging '
        'panel, sturdy adjustable stand, and a multi-LED wide-angle floodlight panel. '
        'This product is assembled in Ethiopia.',
        'The CloudRunner combines sleek modern aesthetics with elite athletic engineering. '
        'Featuring responsive foam midsoles, breathable engineered knit uppers, and '
        'high-traction rubber outsoles.',
        '/static/img/solarflash.jpg', ['/static/img/solarflash1.jpg'], True,
    ),
    (
        'ROZENG RZ-1177 3.1 Multimedia Speaker', 'Accessories', '1.00',
        'A 3.1 channel surround sound multimedia speaker system featuring USB/SD card '
        'functions, an MP3/LED display, Bluetooth connectivity, a remote control, and a '
        '6.5" subwoofer with three satellite speakers. This product is assembled in Ethiopia.',
        'A masterclass in minimalist horology. The Titanium Chronograph features a lightweight '
        'yet incredibly durable titanium case, scratch-resistant sapphire crystal face, '
        'Swiss quartz movement.',
        '/static/img/RZ-1177.jpg', ['/static/img/RZ-11771.jpg'], True,
    ),
    (
        'EthioSolar Portable Hanging Bulb Light Kit',
        'Portable Solar Lighting Systems', '1.99',
        'Compact solar hanging LED bulb with dedicated panel — assembled in Ethiopia.',
        'This compact, energy-efficient solar lighting solution features a bright LED hanging '
        'bulb paired with a dedicated solar panel. It is meticulously assembled in Ethiopia, '
        'providing a reliable, eco-friendly lighting option for homes, outdoor spaces, or '
        'emergency use.',
        '/static/img/photo_17_2026-09-30_20-17-21.jpg', [], False,
    ),
    (
        'EthioSolar Multi-Purpose Searchlight and Bulb Kit',
        'Portable Solar Lighting Systems', '1.99',
        'Handheld LED searchlight/work lamp plus portable bulb and solar charging panel.',
        'A versatile dual-light system consisting of a powerful handheld LED searchlight/work '
        'lamp, a portable bulb, and a solar charging panel. Expertly assembled in Ethiopia, it '
        'offers flexible illumination for households, security tasks, and outdoor adventures.',
        '/static/img/photo_16_2026-09-30_20-17-21.jpg', [], False,
    ),
    (
        'EthioSolar Dual-Panel Power & Work Light Set',
        'Portable Solar Lighting Systems', '1.99',
        'Foldable double-panel solar charger with hanging bulb and heavy-duty flood light.',
        'This robust kit includes a high-capacity foldable double-panel solar charger, an '
        'adjustable hanging bulb, and a heavy-duty portable flood/work light. Assembled in '
        'Ethiopia, it delivers powerful off-grid illumination and rapid solar energy harvesting.',
        '/static/img/photo_14_2026-09-30_20-17-21.jpg', [], False,
    ),
    (
        'EthioSolar Home Power Generator and Three-Bulb Kit',
        'Advanced Solar Power & Generator Kits', '1.99',
        'Off-grid power hub with battery generator, solar panel and three LED bulbs.',
        'A comprehensive off-grid power hub featuring a central battery generator unit with '
        'multiple DC output ports and a built-in panel light, accompanied by a solar panel and '
        'three individual LED bulbs. Proudly assembled in Ethiopia, it provides total home '
        'lighting and device-charging capabilities during power outages.',
        '/static/img/photo_12_2026-09-30_20-17-20.jpg', [], False,
    ),
    (
        'EthioSolar Ergonomic Folding Desk & Task Lamp',
        'Solar Task & Desk Lighting', '1.99',
        'Folding metal task lamp with wide-angle LED panel, powered by a solar panel.',
        'A sleek, modern task light with a folding metal stand and a wide-angle LED panel, '
        'powered by a matching solar panel. Skillfully assembled in Ethiopia, this lamp is '
        'designed for studying, reading, and precise workspace illumination.',
        '/static/img/photo_15_2026-09-30_20-17-21.jpg', [], False,
    ),
    (
        'CH-1222S 1.0 Multi-Function Speaker System',
        'Audio Equipment', '1.99',
        '1200W P.M.P.O portable party speaker with 12" woofer, Bluetooth, TWS and RGB lighting.',
        'A powerful 1200W P.M.P.O portable speaker featuring a 12-inch woofer, Bluetooth '
        'connectivity, TWS support, USB/SD/FM functions, wireless microphone, remote control, '
        'and vibrant RGB lighting effects. This unit is assembled in Ethiopia.',
        '/static/img/photo_2026-09-30_20-16-45.jpg', [], False,
    ),
    (
        'Solar-Powered Portable LED Hanging Bulb',
        'Portable Solar Lighting Systems', '1.99',
        'Outdoor hanging LED bulb with standalone solar panel module and install hook.',
        'An energy-efficient outdoor hanging LED bulb connected to a standalone solar panel '
        'module, featuring a convenient hook for easy installation in tents, patios, or '
        'off-grid living spaces. This product is assembled in Ethiopia.',
        '/static/img/photo_17_2026-09-30_20-17-21_2.jpg', [], False,
    ),
    (
        'Multi-Component Solar Emergency Lighting System',
        'Portable Solar Lighting Systems', '1.99',
        'Home solar kit with multi-LED floodlight/lantern, rechargeable bulb and external panel.',
        'A comprehensive home solar lighting kit containing a multi-LED handheld '
        'floodlight/lantern unit, a portable rechargeable LED bulb, and a high-efficiency '
        'external solar panel. This kit is assembled in Ethiopia.',
        '/static/img/photo_16_2026-09-30_20-17-21_2.jpg', [], False,
    ),
    (
        'Foldable Solar-Powered LED Work Light',
        'Portable Solar Lighting Systems', '1.99',
        'Compact rechargeable utility light with built-in solar panel and flexible wire stand.',
        'A compact, rechargeable utility light featuring a built-in solar panel, flexible wire '
        'stand for easy positioning, and bright LED illumination suitable for outdoor '
        'activities and emergency use. This device is assembled in Ethiopia.',
        '/static/img/photo_15_2026-09-30_20-17-21.jpg', [], False,
    ),
    (
        'Multi-Angle Solar Emergency Floodlight & Bulb Kit',
        'Portable Solar Lighting Systems', '1.99',
        'Dual-panel folding solar charger with hanging bulb and high-intensity floodlight.',
        'A versatile portable lighting setup equipped with an integrated dual-panel folding '
        'solar charger, a hanging LED bulb, and a high-intensity directional floodlight unit. '
        'This product is assembled in Ethiopia.',
        '/static/img/photo_14_2026-09-30_20-17-21.jpg', [], False,
    ),
    (
        'Solar Power Bank & Multi-Bulb Lighting Kit',
        'Advanced Solar Power & Generator Kits', '1.99',
        'Central solar power bank with emergency lighting, three LED bulbs and external panel.',
        'A multi-functional solar energy system featuring a central power bank unit with '
        'built-in emergency lighting, multiple charging output ports, three portable LED bulbs, '
        'and an external photovoltaic solar panel. This kit is assembled in Ethiopia.',
        '/static/img/photo_12_2026-09-30_20-17-20.jpg', [], False,
    ),
    (
        'Solarchange Solar-Powered LED Hand Torch',
        'Portable Solar Lighting Systems', '1.99',
        'Dual-purpose torch with integrated solar panel and side-mounted LED lantern panel.',
        'A durable, dual-purpose flashlight featuring an integrated solar photovoltaic panel '
        'on the body and a side-mounted bright LED lantern panel for versatile handheld or '
        'stationary lighting. This item is assembled in Ethiopia.',
        '/static/img/photo_18_2026-09-30_20-17-21.jpg', [], False,
    ),
]


class Command(BaseCommand):
    help = 'Seed the All Stars showcase catalogue with default categories and products.'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Seeding categories…')
        category_map = {}
        for index, name in enumerate(CATEGORIES):
            category, _ = Category.objects.update_or_create(
                name=name, defaults={'order': index}
            )
            category_map[name] = category

        self.stdout.write('Seeding products…')
        created_count = 0
        updated_count = 0

        for index, row in enumerate(PRODUCTS):
            (name, category_name, price, short_desc,
             description, main_image, gallery, is_featured) = row

            product, created = Product.objects.update_or_create(
                name=name,
                defaults={
                    'category': category_map[category_name],
                    'price': Decimal(price),
                    'short_description': short_desc,
                    'description': description,
                    'external_url': main_image,
                    'is_featured': is_featured,
                    'is_active': True,
                    'sort_order': index,
                },
            )

            if gallery:
                product.gallery_images.all().delete()
                for g_index, url in enumerate(gallery):
                    ProductImage.objects.create(
                        product=product,
                        external_url=url,
                        sort_order=g_index,
                    )

            created_count += int(created)
            updated_count += int(not created)

        self.stdout.write(self.style.SUCCESS(
            f'Done. {created_count} created, {updated_count} updated, '
            f'{len(CATEGORIES)} categories ensured.'
        ))
        self.stdout.write(
            'Next:  python manage.py createsuperuser   →   then open /admin/'
        )