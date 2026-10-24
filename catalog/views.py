from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Category, Product

PRODUCTS_PER_PAGE = 12


def _featured_products(limit=5):
    """Featured products, falling back to the newest active ones."""
    featured = list(
        Product.objects.filter(is_active=True, is_featured=True)
        .select_related('category')
        .order_by('sort_order')[:limit]
    )
    if featured:
        return featured
    return list(
        Product.objects.filter(is_active=True)
        .select_related('category')
        .order_by('sort_order')[:limit]
    )


def home(request):
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()

    products = (
        Product.objects.filter(is_active=True)
        .select_related('category')
        .order_by('sort_order', '-created_at')
    )

    if category_slug:
        products = products.filter(category__slug=category_slug)

    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(short_description__icontains=query)
            | Q(description__icontains=query)
            | Q(category__name__icontains=query)
        )

    paginator = Paginator(products, PRODUCTS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))

    # Check if request is an infinite scroll AJAX call
    is_ajax = (
        request.headers.get('x-requested-with') == 'XMLHttpRequest'
        or request.GET.get('ajax') == '1'
    )

    if is_ajax:
        response = render(request, 'catalog/_product_cards.html', {'page_obj': page_obj})
        response['X-Has-Next'] = 'true' if page_obj.has_next() else 'false'
        response['X-Next-Page'] = str(page_obj.next_page_number()) if page_obj.has_next() else ''
        return response

    context = {
        'featured': _featured_products(),
        'categories': Category.objects.all(),
        'page_obj': page_obj,
        'result_count': paginator.count,
        'q': query,
        'active_category': category_slug,
    }
    return render(request, 'catalog/home.html', context)


def product_detail(request, pk):
    product = get_object_or_404(
        Product.objects.select_related('category'),
        pk=pk,
        is_active=True,
    )

    images = [product.image_url]
    for gallery_item in product.gallery_images.all():
        url = gallery_item.image_url
        if url and url not in images:
            images.append(url)

    try:
        active_index = int(request.GET.get('image', 0))
    except (TypeError, ValueError):
        active_index = 0
    active_index = max(0, min(active_index, len(images) - 1))

    similar = (
        Product.objects.filter(is_active=True, category=product.category)
        .exclude(pk=product.pk)
        .select_related('category')
        .order_by('sort_order')[:3]
    )

    context = {
        'product': product,
        'images': images,
        'active_index': active_index,
        'active_image': images[active_index],
        'similar_products': similar,
    }
    return render(request, 'catalog/product_detail.html', context)