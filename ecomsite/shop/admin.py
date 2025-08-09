from django.contrib import admin
from .models import Product, Order, OrderItem, Category

admin.site.site_header = "Ecommerce Site"
admin.site.site_title = "Digital Shopping"
admin.site.index_title = "Manage Digital Shopping"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class ProductsAdmin(admin.ModelAdmin):

    def change_category_to_default(self, request, queryset):
        # You can't update category="default" since it's a FK,
        # instead you can remove or assign to a default category object if exists
        # So this action may need rethinking or remove it
        pass

    change_category_to_default.short_description = 'Default Category'
    list_display = (
        'title', 'price', 'discount_price',
        'category', 'description'
    )
    search_fields = ('description', )
    actions = ('change_category_to_default',)
    list_editable = (
        'price', 'category',
        'discount_price', 'description',
    )


admin.site.register(Product, ProductsAdmin)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
