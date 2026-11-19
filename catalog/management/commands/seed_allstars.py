"""
Seeds the catalogue with the All Stars / EthioSolar product set.
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
        'Compact rechargeable orange utility light with built-in solar panel, flexible wire stand for easy positioning, and bright LED illumination. Assembled in Ethiopia.',
        'Engineered for off-grid durability with high-efficiency solar panel, rechargeable battery, and multi-mode LEDs. Stand allows hanging, standing, or handheld lighting.',
        '/static/img/solar.jpg', ['/static/img/solar1.jpg'], True,
    ),
    (
        'Multi-Angle Solar light', 'Solar', '1.00',
        'Versatile portable lighting solution with integrated solar charging panel, sturdy adjustable stand, and multi-LED wide-angle floodlight. Assembled in Ethiopia.',
        'Featuring an adjustable multi-angle bracket and wide-dispersion LED panel, this light provides high lumen output for workspaces, security, and homes.',
        '/static/img/solarflash.jpg', ['/static/img/solarflash1.jpg'], True,
    ),
    (
        'ROZENG RZ-1177 3.1 Multimedia Speaker', 'Audio Equipment', '1.00',
        '3.1 channel surround sound speaker system with USB/SD, MP3/LED display, Bluetooth, remote control, and 6.5" subwoofer with 3 satellite speakers. Assembled in Ethiopia.',
        'High-definition home audio experience featuring 90W total output (45W + 15Wx3), low-distortion amplifier circuit, Bluetooth streaming, USB/SD playback, FM radio, and remote control.',
        '/static/img/RZ-1177.jpg', ['/static/img/RZ-11771.jpg'], True,
    ),
    (
        'EthioSolar Portable Hanging Bulb Light Kit',
        'Portable Solar Lighting Systems', '1.99',
        'Compact solar hanging LED bulb with dedicated panel — assembled in Ethiopia.',
        'This compact, energy-efficient solar lighting solution features a bright LED hanging bulb paired with a dedicated solar panel. Assembled in Ethiopia.',
        '/static/img/photo_17_2026-09-30_20-17-21.jpg', [], False,
    ),
    (
        'EthioSolar Multi-Purpose Searchlight and Bulb Kit',
        'Portable Solar Lighting Systems', '1.99',
        'Handheld LED searchlight/work lamp plus portable bulb and solar charging panel.',
        'A versatile dual-light system consisting of a powerful handheld LED searchlight, portable bulb, and solar charging panel. Assembled in Ethiopia.',
        '/static/img/photo_16_2026-09-30_20-17-21.jpg', [], False,
    ),
    (
        'EthioSolar Dual-Panel Power & Work Light Set',
        'Portable Solar Lighting Systems', '1.99',
        'Foldable double-panel solar charger with hanging bulb and heavy-duty flood light.',
        'Robust kit includes a high-capacity foldable double-panel solar charger, adjustable hanging bulb, and heavy-duty portable work light. Assembled in Ethiopia.',
        '/static/img/photo_14_2026-09-30_20-17-21.jpg', [], False,
    ),
    (
        'EthioSolar Home Power Generator and Three-Bulb Kit',
        'Advanced Solar Power & Generator Kits', '1.99',
        'Off-grid power hub with battery generator, solar panel and three LED bulbs.',
        'Comprehensive off-grid power hub featuring central battery generator unit with DC output ports, solar panel, and three LED bulbs. Assembled in Ethiopia.',
        '/static/img/photo_12_2026-09-30_20-17-20.jpg', [], False,
    ),
    (
        'EthioSolar Ergonomic Folding Desk & Task Lamp',
        'Solar Task & Desk Lighting', '1.99',
        'Folding metal task lamp with wide-angle LED panel, powered by a solar panel.',
        'Modern task light with folding metal stand and wide-angle LED panel, powered by a matching solar panel. Assembled in Ethiopia.',
        '/static/img/photo_15_2026-09-30_20-17-21.jpg', [], False,
    ),
    (
        'CH-1222S 1.0 Multi-Function Speaker System',
        'Audio Equipment', '1.99',
        '1200W P.M.P.O portable party speaker with 12" woofer, Bluetooth, TWS and RGB lighting.',
        'Powerful 1200W P.M.P.O portable speaker featuring a 12-inch woofer, Bluetooth connectivity, TWS support, USB/SD/FM functions, microphone, and RGB lights. Assembled in Ethiopia.',
        '/static/img/photo_2026-09-30_20-16-45.jpg', [], False,
    ),
    (
        'Solar-Powered Portable LED Hanging Bulb',
        'Portable Solar Lighting Systems', '1.99',
        'Outdoor hanging LED bulb with standalone solar panel module and install hook.',
        'Energy-efficient outdoor hanging LED bulb connected to a standalone solar panel module with hook for easy installation. Assembled in Ethiopia.',
        '/static/img/photo_17_2026-09-30_20-17-21_2.jpg', [], False,
    ),
    (
        'Multi-Component Solar Emergency Lighting System',
        'Portable Solar Lighting Systems', '1.99',
        'Home solar kit with multi-LED floodlight/lantern, rechargeable bulb and external panel.',
        'Comprehensive home solar lighting kit containing a multi-LED handheld lantern unit, rechargeable LED bulb, and high-efficiency solar panel. Assembled in Ethiopia.',
        '/static/img/photo_16_2026-09-30_20-17-21_2.jpg', [], False,
    ),
    (
        'Foldable Solar-Powered LED Work Light',
        'Portable Solar Lighting Systems', '1.99',
        'Compact rechargeable utility light with built-in solar panel and flexible wire stand.',
        'Compact rechargeable utility light featuring a built-in solar panel, flexible wire stand, and bright LED illumination. Assembled in Ethiopia.',
        '/static/img/photo_15_2026-09-30_20-17-21.jpg', [], False,
    ),
    (
        'Multi-Angle Solar Emergency Floodlight & Bulb Kit',
        'Portable Solar Lighting Systems', '1.99',
        'Dual-panel folding solar charger with hanging bulb and high-intensity floodlight.',
        'Versatile portable lighting setup equipped with an integrated dual-panel folding solar charger, hanging LED bulb, and directional floodlight. Assembled in Ethiopia.',
        '/static/img/photo_14_2026-09-30_20-17-21.jpg', [], False,
    ),
    (
        'Solar Power Bank & Multi-Bulb Lighting Kit',
        'Advanced Solar Power & Generator Kits', '1.99',
        'Central solar power bank with emergency lighting, three LED bulbs and external panel.',
        'Multi-functional solar energy system featuring central power bank unit with built-in lighting, output ports, three LED bulbs, and solar panel. Assembled in Ethiopia.',
        '/static/img/photo_12_2026-09-30_20-17-20.jpg', [], False,
    ),
    (
        'Solarchange Solar-Powered LED Hand Torch',
        'Portable Solar Lighting Systems', '1.99',
        'Dual-purpose torch with integrated solar panel and side-mounted LED lantern panel.',
        'Durable flashlight featuring an integrated solar photovoltaic panel on the body and side-mounted LED lantern panel. Assembled in Ethiopia.',
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
                    'short_description': (short_desc or '')[:190],  # Strictly < 200 chars
                    'description': description or '',
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

        # Ensure admin user exists
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user, _ = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com'})
        user.set_password('AdminPass123!')
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()

        self.stdout.write(self.style.SUCCESS(
            f'Done. {created_count} created, {updated_count} updated. Admin user ready.'
        ))
