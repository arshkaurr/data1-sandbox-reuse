from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Location)



admin.site.register(Pricing)
admin.site.register(Category)


class LinkAdmin(admin.ModelAdmin):
    # fields = ['url','category']
    list_display = ('category','order','text')

admin.site.register(Link, LinkAdmin)



class LinkAdmin_product(admin.ModelAdmin):
    # fields = ['url','category']
    list_display = ('shopify_handle','order','id','visible','location','classifier','product_type')
    list_filter = ['location','order','visible','product_type__category','product_type']

admin.site.register(Product, LinkAdmin_product)


class LinkAdmin_variant(admin.ModelAdmin):
    # fields = ['url','category']
    list_display = ('variant','product','id','price')
    list_filter = ['product__location','product__product_type__category','product__product_type']
admin.site.register(Variant, LinkAdmin_variant)



class LinkAdmin_producttype(admin.ModelAdmin):
    list_display = ('product_type','code','category')
    list_filter = []
admin.site.register(ProductType, LinkAdmin_producttype)
