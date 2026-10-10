from .models import Category


def navigation(request):
    """Makes the footer category list available on every page."""
    return {
        'nav_categories': Category.objects.all()[:8],
    }