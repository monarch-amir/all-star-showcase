from decimal import Decimal

from django.db import models
from django.urls import reverse
from django.utils.text import slugify

FALLBACK_IMAGE = '/static/img/placeholder.svg'


class ImageSourceMixin(models.Model):
    """
    Dual-source image support: an admin can either upload a file through the
    admin panel *or* paste an external URL / static path.
    """

    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        help_text='Upload an image file. Used only when no external URL is set.',
    )
    external_url = models.CharField(
        max_length=500,
        blank=True,
        help_text='External URL or a static path, e.g. /static/img/solar.jpg',
    )

    class Meta:
        abstract = True

    @property
    def image_url(self) -> str:
        if self.external_url:
            return self.external_url
        if self.image:
            try:
                return self.image.url
            except ValueError:
                return FALLBACK_IMAGE
        return FALLBACK_IMAGE


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True, blank=True)
    order = models.PositiveIntegerField(
        default=0, help_text='Lower numbers appear first in the filter bar.'
    )

    class Meta:
        ordering = ('order', 'name')
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f'/?category={self.slug}'


class Product(ImageSourceMixin):
    name = models.CharField(max_length=120)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,          # blocks deleting a category that is in use
        related_name='products',
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    short_description = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    is_featured = models.BooleanField(
        default=False,
        help_text='Featured products are shown in the home carousel (5 max recommended).',
    )
    is_active = models.BooleanField(
        default=True, help_text='Uncheck to hide this product from the public showcase.'
    )
    sort_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('sort_order', '-created_at')
        indexes = [models.Index(fields=['category', 'is_active'])]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:product_detail', args=[self.pk])


class ProductImage(ImageSourceMixin):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='gallery_images'
    )
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('sort_order', 'id')
        verbose_name = 'gallery image'
        verbose_name_plural = 'gallery images'

    def __str__(self):
        return f'{self.product.name} — image #{self.pk or "new"}'