from django.urls import path

from pricing.views import *

app_name='pricing'

urlpatterns = [
    path('portal/<slug:location>/', pricing_portal, name='portal'),
    path('portal_legacy/<slug:location>/', pricing_portal_legacy, name='pricing_portal_legacy'),
    path('raw/<slug:location>/', raw, name='raw'),
    path('stats/<slug:location>/', stats, name='stats'),
    path('submit/', pricing_submit, name='submit'),

    path('my_pricing_table/', my_pricing_table, name='my_pricing_table'),
    path('delete/<int:record>/', delete_record, name='delete_record'),
    path('delete_submit/', delete_submit, name='delete_submit'),

    # USED FOR RON / MANUALLY PRICING OUT BULK PRICED ITEMS
    # path('temp_barcode/', temp_barcode, name='temp_barcode'),
    # TESTER FOR RETAIL RESOUCES
    path('tester/', tester, name='tester'),

    path('update_pos/', update_pos, name='update_pos'),
    path('update_pos/color_wheel/', color_wheel_data, name='color_wheel_data'),
    path('update_pos_item/', update_pos_item, name='update_pos_item'),
    path('update_pos_item_test/', update_pos_item_test, name='update_pos_item_test'),
    path('generate_standard_variants/', generate_standard_variants, name='generate_standard_variants'),

]
