from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, FileResponse, JsonResponse
from django.db.models import Sum, Avg, Count, Min, Max, ExpressionWrapper, F, DecimalField, DateTimeField
from django.db.models.functions import Trunc, Extract
import requests
from pricing.functions import barcode_reuse_1, color_wheel_2021, color_wheel_2022, drop_price, data1_handle_process, shopify_handle_process

from pricing.models import *
import json

from datetime import datetime, timedelta
from django.utils import timezone
import pytz

from visitors.functions import *

from visitors.functions import start_end_date

import pandas as pd

from time import sleep
from collections import defaultdict

from local_settings import *


def wants_json_response(request):
    fmt = request.GET.get('format', '')
    if fmt.lower() == 'json':
        return True
    accept_header = request.headers.get('Accept', '')
    return 'application/json' in accept_header.lower()


def pricing_portal_legacy(request, location):
    #authentication
    if not request.user.is_authenticated:
        return redirect('HOME')

    # LOCATION SLUG CHECK
    if location.upper() in ['TRMC', 'TRC', 'TRMC', 'RMC']:
        LOCATION = 'T'
    elif location.upper() in ['IRC', 'IRMC']:
        LOCATION = 'I'
    else:
        return(redirect('/'))

    products_std = [i.shopify_handle for i in Product.objects.filter(location=Location.objects.get(location=LOCATION), classifier__in=['W','R','G','B','Y','L','O'])]
    products_unit = {}
    V = Variant.objects.filter(product__location=Location.objects.get(location=LOCATION), product__classifier='U', visible=True).values('variant','title','price').order_by('title')

    # Create a SET of the unique IDS
    products_ids = set([x['variant'][0:5] for x in V])
    #Declare a blank Dict and Add the unique IDS to the dict with empty lists()
    products_unit_test = {}
    for i in products_ids:
        products_unit_test[i] = list()

    for i in V:
        products_unit_test[ i['variant'][:5] ].append([  i['variant'],i['title'],f"{i['price']:.2f}"  ])

########################### TEST SEGMENT END

    color_reference = {'W':'White', 'R':'Red', 'B':'Blue', 'Y':'Yellow', 'G':'Green', 'O':'Orange', 'L':'Lavender'}
    CC = color_wheel_2021(timezone.now())
    CColor = color_reference[CC]
    print(CC,CColor)

    context = {
        'products_std': products_std,
        'products_unit': products_unit_test,
        'CColor': CColor,
        'CC': CC,
        'LOCATION': LOCATION,
    }

    if wants_json_response(request):
        return JsonResponse(context, json_dumps_params={'default': str})

    template = 'pricing/pricing_trmc.html' if LOCATION == 'T' else 'pricing/pricing_irc.html'
    return render(request, template, context)








#######&#$^#&*^$&*#^$##################################
#######&#$^#&*^$&*#^$##################################
def pricing_portal(request, location):
    #authentication
    if not request.user.is_authenticated:
        return redirect('HOME')

    # LOCATION SLUG CHECK
    if location.upper() in ['TRMC', 'TRC', 'TRMC', 'RMC']:
        LOCATION = 'T'
        TEXT = 'TRMC : ReUse MEGACENTER'
    elif location.upper() in ['IRC', 'IRMC']:
        LOCATION = 'I'
        TEXT = 'IRC : Ithaca ReUse Center'
    else:
        return(redirect('/'))

    color_reference = {'W':'White', 'R':'Red', 'B':'Blue', 'Y':'Yellow', 'G':'Green', 'O':'Orange', 'L':'Lavender'}
    CC = color_wheel_2021(timezone.now())
    CColor = color_reference[CC]

    products_white = Product.objects.filter(visible=True, location=Location.objects.get(location=LOCATION), classifier='W').values('shopify_handle','title').order_by('order', 'id')
    products_color = Product.objects.filter(visible=True, location=Location.objects.get(location=LOCATION), classifier=CC).values('shopify_handle','title').order_by('order', 'id')
    products_unit = Product.objects.filter(visible=True, location=Location.objects.get(location=LOCATION), classifier='U').values('shopify_handle','title').order_by('order', 'id')

    V = Variant.objects.filter(product__location=Location.objects.get(location=LOCATION), product__classifier='U', visible=True).values('variant','title','price').order_by('title')

    # Create a SET of the unique IDS
    products_ids = set([x['variant'][0:5] for x in V])
    #Declare a blank Dict and Add the unique IDS to the dict with empty lists()
    products_unit_test = {}
    for i in products_ids:
        products_unit_test[i] = list()

    for i in V:
        products_unit_test[ i['variant'][:5] ].append([  i['variant'],i['title'],f"{i['price']:.2f}"  ])

    context = {
        'products_white': products_white,
        'products_color': products_color,
        'products_unit': products_unit,
        'products_unit_test': products_unit_test,
        'CColor': CColor,
        'CC': CC,
        'LOCATION': LOCATION,
        'TEXT': TEXT
    }

    if wants_json_response(request):
        json_payload = context.copy()
        json_payload['products_white'] = list(products_white)
        json_payload['products_color'] = list(products_color)
        json_payload['products_unit'] = list(products_unit)
        return JsonResponse(json_payload, json_dumps_params={'default': str})

    return render(request, 'pricing/pricing.html', context)























def pricing_submit(request):
    #authentication
    if not request.user.is_authenticated:
        return redirect('HOME')

    json_requested = wants_json_response(request)

    try:
        VARIANT = request.GET['variant']
        PRINT = bool(int(request.GET['print']))
        INVENTORY = bool(int(request.GET['inventory']))
        QUANTITY = int(request.GET['quantity'])

        color_reference = {'W':'WHITE','U':'WHITE (Unit)', 'R':'RED', 'B':'BLUE', 'Y':'YELLOW', 'G':'GREEN', 'O':'ORANGE', 'L':'LAVENDER'}

        V = Variant.objects.get(variant=VARIANT)

        if V.title[0] == '$':
            TITLE = str(V.product)
        else:
            TITLE = str(V.title)

        #Submit to DB!!!
        #########IMPORTANT : ONLY SUBMIT IF inventory=True; Rest getting depricated
        if INVENTORY:
            STAFF_ID = str(request.user.email).split('@fingerlakesreuse.org')[0]
            submission = Pricing.objects.create(variant=V, quantity=QUANTITY, staff_id=STAFF_ID, print=PRINT, inventory=INVENTORY)

        #GENERATE CODE
	    # HARDCODE EMERGENCY #JAN27 2022
        if json_requested:
            return JsonResponse({
                'status': 'ok',
                'variant': VARIANT,
                'print': PRINT,
                'inventory': INVENTORY,
                'quantity': QUANTITY,
                'title': TITLE,
                'color': color_reference[V.variant[0]]
            }, json_dumps_params={'default': str})

        X = barcode_reuse_1(VARIANT, V.price, TITLE, color_reference[V.variant[0]], ' '.join(VARIANT[:5]), QUANTITY)
        return FileResponse(X, as_attachment=False, filename="barcode.pdf")

    except:

        if json_requested:
            return JsonResponse({'status': 'error'}, status=400)

        E = barcode_reuse_1('ERORR', 0, 'ERROR', 'ERROR', 'ERROR', 1)
        return FileResponse(E, as_attachment=False, filename="barcode-ERROR.pdf")

    # barcode_reuse_1(VARIANT,PRICE,TITLE, COLOR, HANDLE, QUANTITY)




########
def my_pricing_table(request):
    if not request.user.is_authenticated:
        return redirect('HOME')

    response_html = '<table id="mainTable" class="table table-sm"><thead><tr><th>ID</th><th>Date/Time</th><th>Tag</th><th>Product</th><th>Variant</th><th>Price</th><th>Quantity</th><th>DELETE</th></tr></thead><tbody>'
    classifier_choices = {'U':'Unit','W':'White','Y':'Yellow','R':'Red','O':'Orange','B':'Blue','G':'Green','L':'Lavender'}
    json_requested = wants_json_response(request)
    rows = []


    QUERY = Pricing.objects.filter(staff_id=request.user.email.split('@')[0], inventory=True, deleted=False)\
        .order_by('-timestamp')[:20]\
        .values('variant__product__classifier','variant__title','timestamp','variant__product__title','variant__price', 'quantity', 'id')

    for i in QUERY:
        timestamp_eastern = i['timestamp'].astimezone(tz=pytz.timezone('US/Eastern'))
        timestamp_display = datetime.strftime(timestamp_eastern,'%a %d/%m/%y - %I:%M %p')
        # IF the timestamp is not less than a day old, render the delete button > so that folks can delete it if needed.
        if i['timestamp'] > timezone.now()-timedelta(days=1):
            delete_button_html = f'<a target="_new" href="{reverse("pricing:delete_record", kwargs={"record":i["id"]})}" class="btn btn-success btn-sm" role="button" aria-pressed="true">DEL</a>'
        else:
            delete_button_html = '-'
        response_html += f"<tr><td>{i['id']}</td><td>{timestamp_display}</td><td>{classifier_choices[i['variant__product__classifier']]}</td><td>{i['variant__product__title']}</td><td>{i['variant__title']}</td><td>{i['variant__price']}</td><td>{i['quantity']}</td><td>{delete_button_html}</td>"
        rows.append({
            'id': i['id'],
            'timestamp': timestamp_eastern.isoformat(),
            'timestamp_display': timestamp_display,
            'tag': classifier_choices[i['variant__product__classifier']],
            'product': i['variant__product__title'],
            'variant': i['variant__title'],
            'price': i['variant__price'],
            'quantity': i['quantity'],
            'delete_url': reverse("pricing:delete_record", kwargs={"record":i["id"]}),
            'can_delete': i['timestamp'] > timezone.now()-timedelta(days=1),
        })

    response_html += f'</tbody></table>'
    if json_requested:
        return JsonResponse({'rows': rows}, json_dumps_params={'default': str})
    return HttpResponse(response_html)




def delete_record(request, record):
    if not request.user.is_authenticated:
        return redirect('HOME')

    R = Pricing.objects.filter(id=record)\
        .values('deleted','id','staff_id','timestamp','variant__variant', 'variant__product__product_type__product_type','quantity')[0]

    if R['staff_id'] != request.user.email.split('@')[0]:
        return HttpResponse('NOT YOUR USER ACCOUNT')

    if R['timestamp'] < timezone.now()-timedelta(days=1):
        return HttpResponse('THIS RECORD IS TOO OLD TO DELETE')


    return_dict = {'R':R}
    return render(request, 'pricing/delete_record.html', return_dict)




def delete_submit(request):
    try:
        record = int(request.POST.get('id'))
        print(record)

        R = Pricing.objects.filter(id=record)[0]
        print(vars(R))
        R.deleted = True
        R.save()
        return redirect( reverse('pricing:delete_record',kwargs={"record":record }) )
    except:
        return HttpResponse('ERROR OCCURED')

# ######### USE THIS FOR PRITING TAGS TEMPORARILY
# def temp_barcode(request):
#     E = barcode_reuse_1('K04F03:UTHOW1.00GE06',3.0,'Buy 4 for $3', 'BULK', 'HOUSEWARES', 1)
#     return FileResponse(E, as_attachment=False, filename="barcode-ERROR.pdf")


#################################
# START
#################################
def raw(request,location):
    #authentication
    if not request.user.is_authenticated:
        return redirect('HOME')

    # LOCATION SLUG CHECK
    if location.upper() in ['TRMC', 'TRC', 'TRMC', 'RMC']:
        LOCATION = 'T'
        location = 'TRMC'
    elif location.upper() in ['IRC', 'IRMC']:
        LOCATION = 'I'
        location = 'IRC'
    else:
        return(redirect('HOME'))

    #GET the GET values from the view or else generate them
    start_date, end_date = start_end_date(request.GET)

    P = Pricing.objects.filter(timestamp__gte=start_date, timestamp__lte=end_date ,variant__product__location=Location.objects.get(location=LOCATION), inventory=True, deleted=False)\
    .values('variant__variant').annotate(TOTAL_QUANTITY=Sum('quantity'), TOTAL_VALUE=ExpressionWrapper(Sum('quantity')*F('variant__price'), output_field=DecimalField())   )\
    .values('variant__variant','variant__product__product_type__product_type', 'variant__product__classifier', 'variant__product__title', 'variant__title', 'variant__price', 'TOTAL_QUANTITY', 'TOTAL_VALUE')






    context = {
        'location': location,
        'P': P,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
    }

    if wants_json_response(request):
        json_payload = context.copy()
        json_payload['P'] = list(P)
        return JsonResponse(json_payload, json_dumps_params={'default': str})

    return render(request, 'pricing/raw.html', context)




######### STATS PAGE  ##################
def stats(request, location=''):
    #authentication
    if not request.user.is_authenticated:
        return redirect('HOME')
    #GET the GET values from the view or else generate them
    start_date, end_date = start_end_date(request.GET)
    # LOCATION SLUG CHECK
    if location.upper() in ['TRMC', 'TRC', 'TRMC', 'RMC']:
        LOCATION = 'T'
        location = 'TRMC'
    elif location.upper() in ['IRC', 'IRMC']:
        LOCATION = 'I'
        location = 'IRC'
    else:
        return(redirect('HOME'))

    pricing = Pricing.objects.filter(timestamp__gte=start_date, timestamp__lte=end_date ,variant__product__location=Location.objects.get(location=LOCATION), inventory=True, deleted=False)

    Qu = Pricing.objects.filter(timestamp__gte=start_date, timestamp__lte=end_date ,variant__product__location=Location.objects.get(location=LOCATION), inventory=True, deleted=False)\

    total_items = Qu.aggregate(total_items=Sum('quantity'))['total_items']
    total_pricing_value = Qu.aggregate(TOTAL_VALUE=Sum(ExpressionWrapper(F('quantity')*F('variant__price'), output_field=DecimalField())))['TOTAL_VALUE']
    items_per_submission = Qu.aggregate(items_per_submission=Avg('quantity'))['items_per_submission']

    #Product Type Breakdown
    PT = Qu.values('variant__product__product_type__product_type').annotate(
        PT = F('variant__product__product_type__product_type'),
        PRICING_VALUE = Sum(ExpressionWrapper(F('quantity')*F('variant__price'), output_field=DecimalField())),
        TOTAL_ITEMS = Sum('quantity'),
        COUNT = Count('variant__product__product_type__product_type'),
        ITEM_SUBMISSIONS = Avg('quantity'),
        AVG = Avg('variant__price'),
        CAT = F('variant__product__product_type__category__category'),
    )

    #Product Type Breakdown
    ST = Qu.values('staff_id').annotate(
        ST = F('staff_id'),
        PRICING_VALUE = Sum(ExpressionWrapper(F('quantity')*F('variant__price'), output_field=DecimalField())),
        TOTAL_ITEMS = Sum('quantity'),
        COUNT = Count('variant__product__product_type__product_type'),
        ITEM_SUBMISSIONS = Avg('quantity'),
        AVG = Avg('variant__price'),
    )
######################
# OCT 2021 - BIG BREAKTHROUGH   - - - NEEDS POSSIBLY MORE ATTENTION
# TRIED TO DO IT THE DJANGO-PIVOT WAY BUT FAILED, REVERTING TO PANDAS
    # DT = Qu.annotate(date=Trunc('timestamp', 'day', tzinfo=pytz.timezone('US/Eastern')),
    #     product_type=F('variant__product__product_type__product_type')).values('date','product_type').annotate(quantity_sum=Sum('quantity')).order_by('date')
    #
    # DT = Qu.annotate(date=Trunc('timestamp', 'day', tzinfo=pytz.timezone('US/Eastern')),
    #     product_type=F('variant__product__product_type__product_type')).values('date','product_type', 'quantity')


    x = pricing.annotate(date=Trunc('timestamp','day', output_field=DateTimeField())).values('date').annotate(quantity=Sum('quantity'), product_type=F('variant__product__product_type__product_type')).order_by('date')

    cats = [i['product_type'] for i in ProductType.objects.all().order_by('category__category').values('product_type')  ]
    print(cats)
    tupdict = defaultdict(int)
    for i in x: tupdict[(    i['date'], i['product_type']   )] = i['quantity']

    DT_table=[]
    for i,date in enumerate( sorted(  list( set( i['date'] for i in x )  )   )   ):
        DT_table.append({'date': date})
        for j in cats: DT_table[i][j] = tupdict[(date , j)]

#     for i in DT_table: print(i)
# ####################
#
#     print(['cats'] + cats)


    json_dt = []
    for row in DT_table:
        json_row = row.copy()
        if isinstance(json_row.get('date'), datetime):
            json_row['date'] = json_row['date'].isoformat()
        json_dt.append(json_row)

    try:
        avg_item_price = total_pricing_value / total_items
    except:
        avg_item_price = ''

    context = {
        'location': location,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'total_items': total_items,
        'total_pricing_value': total_pricing_value,
        'pricing_submissions': Qu.count(),
        'avg_item_price': avg_item_price,
        'items_per_submission': items_per_submission,
        'PT': PT,
        'ST': ST,
        'DT': DT_table,
        'cats': ['date'] + cats,
    }

    if wants_json_response(request):
        json_payload = context.copy()
        json_payload['PT'] = list(PT)
        json_payload['ST'] = list(ST)
        json_payload['DT'] = json_dt
        return JsonResponse(json_payload, json_dumps_params={'default': str})

    return render(request, 'pricing/stats.html', context)

######################
# NEW HOME > RENDERS THE LINKS FOR HOME  #TOVA

def template_home(request):
    #authentication
    if not request.user.is_authenticated:
        return_dict = dict()
    else:
        L = Link.objects
        return_dict = {
            'L_Q' : L.filter(category='Q').order_by('order'),
            'L_A' : L.filter(category='A').order_by('order'),
            'L_C' : L.filter(category='C').order_by('order'),
            'L_E' : L.filter(category='E').order_by('order'),
        }

    return render(request, 'pricing/spark_base.html', return_dict)



#####################
# TESTER FOR NEW RETAIL RESOURCES

def tester(request):
    return render(request,'pricing/tester.html')



def update_pos(request):

    #authentication
    if not request.user.is_staff:
        return redirect('HOME')

    try:
        date = datetime.strptime(request.GET['date'], '%Y-%m-%d').replace(tzinfo=pytz.timezone('US/Eastern'))
    except:
        date = timezone.now().astimezone(pytz.timezone('US/Eastern'))

    all_products_query = Product.objects.values('location__location', 'id', 'shopify_handle', 'classifier', 'product_type__product_type', 'product_type__category__category')
    all_products = dict()
    #Create HASH TABLE OF Query for JS LOOKUP DB
    for i in all_products_query:
        all_products[i['shopify_handle']] = i


    try:
        correction = int(float(request.GET['correction']))
    except:
        correction = 0


    return_dict = {

        'all_products':  all_products,
        'color_rotations' : color_wheel_2022(date),  #{'pricing':'B', 'hold': 'L', '25': 'G', '50':'R', '75':'O', 'reset':'Y'},
        'date':date.strftime('%Y-%m-%d'),
    }

    return render(request, 'pricing/update_pos.html', return_dict)



def color_wheel_data(request):
    if not request.user.is_staff:
        return JsonResponse({'detail': 'Authentication required'}, status=403)

    try:
        date = datetime.strptime(request.GET['date'], '%Y-%m-%d').replace(tzinfo=pytz.timezone('US/Eastern'))
    except:
        date = timezone.now().astimezone(pytz.timezone('US/Eastern'))

    rotations = color_wheel_2022(date)

    return JsonResponse({
        'date': date.strftime('%Y-%m-%d'),
        'color_rotations': rotations,
    }, json_dumps_params={'default': str})




def update_pos_item(request):
    if not request.user.is_staff:
        return HttpResponse('500 - Unauthenticated')

    try:
        sru = bool(int(float(request.GET.get('sru',0))))
    except:
        sru = False
    try:
        handle = request.GET['handle']
    except:
        return HttpResponse('400 - Problem with HANDLE')
    try:
        discount = int(float(request.GET.get('discount', 0)))
        if discount > 100:
            discount = 100
        elif discount < 0:
            discount = 0
    except:
        discount = 0

    new_ratio = 1 - discount/100

    tags = datetime.now(pytz.timezone('US/Eastern')).strftime("P-%Y-%m-%d-%H-%M-%S")
    if sru==True:
        tags+=',SRUE'

    return HttpResponse(drop_price(handle,new_ratio,tags))



def update_pos_item_test(request):
    sleep(2)
    x = timezone.now().astimezone(pytz.timezone('US/Eastern'))
    print(request.GET.get('handle',-1))
    print(request.GET.get('discount',-1))
    print(request.GET.get('sru',-1))
    return HttpResponse(f'WORKING {x}')



def generate_standard_variants(request):

    if not request.user.is_staff:
        return HttpResponse('500 - Unauthenticated')

    MESSAGE = ''

    shopify_handle = str(request.POST.get('shopify_handle', '')).strip().upper()
    data1_handle = str(request.POST.get('data1_handle', '')).strip().upper()

    if shopify_handle!='' and data1_handle != '':
        MESSAGE += 'Shopify handle and data1 handles provided. Please only provide one handle<br><br>'

    elif data1_handle=='' and shopify_handle=='':
        # MESSAGE += 'NO INPUT RECEIVED! - both fields blank <br><br>'
        pass

    elif data1_handle:
        MESSAGE += data1_handle_process(data1_handle)

    elif shopify_handle:
        MESSAGE += shopify_handle_process(shopify_handle)
    else:
        MESSAGE += 'UNKNOW ERROR <br><br>'


    return render(request,'pricing/generate_standard_variants.html',{'MESSAGE': MESSAGE} )

    return HttpResponse(log)
