from django.contrib import admin

from mm.models import Movement,Pallet
# Register your models here.
# admin.site.register(Movement)
# admin.site.register(Pallet)


class LinkAdmin_movement(admin.ModelAdmin):
    # fields = ['url','category']
    list_display = ('id','timestamp','staff_id','origin_type','origin_location','destination_type','destination_location')
    list_filter = ('origin_type','origin_location','destination_type','destination_location')

admin.site.register(Movement, LinkAdmin_movement)


class LinkAdmin_pallet(admin.ModelAdmin):
    # fields = ['url','category']
    list_display = ('movement','product_type','quantity')


admin.site.register(Pallet, LinkAdmin_pallet)
