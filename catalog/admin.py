from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product, ProductImage

admin.site.site_header = 'All Stars Control Panel'
admin.site.site_title = 'All Stars Admin'
admin.site.index_title = 'Catalogue Management'


# ----------------------------------------------------------------------
# Inlines
# ----------------------------------------------------------------------
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('preview', 'image', 'external_url', 'sort_order')
    readonly_fields = ('preview',)
    ordering = ('sort_order', 'id')

    @admin.display(description='Preview')
    def preview(self, obj):
        if not obj or not obj.pk:
            return '—'
        return format_html(
            '<img src="{}" style="height:56px;width:56px;object-fit:cover;'
            'border-radius:6px;border:1px solid #e2e8f0;">',
            obj.image_url,
        )


# ----------------------------------------------------------------------
# Categories
# ----------------------------------------------------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'product_count', 'order')
    list_display_links = ('name',)
    list_editable = ('order',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')

    @admin.display(description='Products')
    def product_count(self, obj):
        return obj.products.count()


# ----------------------------------------------------------------------
# Products
# ----------------------------------------------------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'thumbnail', 'name', 'category', 'price',
        'is_featured', 'is_active', 'sort_order',
    )
    list_display_links = ('name',)
    list_editable = ('is_featured', 'is_active', 'sort_order')
    list_filter = ('is_active', 'is_featured', 'category')
    search_fields = ('name', 'short_description', 'description')
    inlines = [ProductImageInline]
    save_on_top = True
    list_per_page = 25
    ordering = ('sort_order', '-created_at')

    fieldsets = (
        ('Identity', {
            'fields': ('name', 'category', 'price', 'sort_order')
        }),
        ('Copy', {
            'fields': ('short_description', 'description')
        }),
        ('Primary image', {
            'fields': ('image', 'external_url'),
            'description': 'Upload a file, or paste a URL / static path. '
                           'The external URL wins when both are set.',
        }),
        ('Visibility', {
            'fields': ('is_featured', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    actions = ('mark_featured', 'unmark_featured', 'activate', 'deactivate')

    # ------------------------- columns -------------------------
    @admin.display(description='')
    def thumbnail(self, obj):
        return format_html(
            '<img src="{}" style="height:44px;width:44px;object-fit:cover;'
            'border-radius:8px;border:1px solid #e2e8f0;">',
            obj.image_url,
        )

    # ------------------------- actions -------------------------
    @admin.action(description='Add to home carousel')
    def mark_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} product(s) added to the carousel.')

    @admin.action(description='Remove from home carousel')
    def unmark_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} product(s) removed from the carousel.')

    @admin.action(description='Show in public showcase')
    def activate(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} product(s) published.')

    @admin.action(description='Hide from public showcase')
    def deactivate(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} product(s) hidden.')

    # ----------------------- housekeeping ----------------------
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        featured = Product.objects.filter(is_featured=True).count()
        if featured > 5:
            self.message_user(
                request,
                f'Note: {featured} products are flagged as featured. '
                'Only the first 5 are shown in the home carousel.',
                level=30,   # WARNING
            )