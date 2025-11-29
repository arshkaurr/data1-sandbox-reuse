from .models import *
from time import sleep
from local_settings import *
import json
import requests

#Reportlab - Barcodes
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import qr
from reportlab.lib.units import inch
import io

#Color tag rotation functions
from datetime import datetime, timedelta
from pytz import timezone

from time import sleep
# from pricing.functions import S_URL


def fill_variants_color(handle):
    #Step 1: Try and get the handle and report the Response code
    print(S_URL)
    request = requests.get(S_URL + 'products.json', params={'handle':handle})
    print(f'Request Status Code of "{handle}": {request.status_code}')
    response = json.loads(request.text)
    #Step 2: Print out a list of titles that it received
    #Step 3: Add each of them to the database
    try:
        product = response['products'][0]
        Q = Product.objects.get(shopify_handle = handle.upper().strip())
        print(Q, 'now going to add them to the database')
        sleep(4)
        for i in product['variants']:
            print(f'{i["id"]}  {i["title"]}', end='\t')
            try:
                QQ = Variant(product=Q, title=i['title'], price=float(i['price']), variant=i['sku']).save()

            except:
                print('ERROR OCCURER ^ - moving to next')

    except:
        print('FAILED - no product found / Error occured')

    print('\n DONE')
    pass





def fill_variants_unit(handle):
    #Step 1: Try and get the handle and report the Response code
    print(S_URL)
    request = requests.get(S_URL + 'products.json', params={'handle':handle})
    print(f'Request Status Code of "{handle}": {request.status_code}')
    response = json.loads(request.text)
    #Step 2: Print out a list of titles that it received
    #Step 3: Add each of them to the database
    try:
        product = response['products'][0]
        Q = Product.objects.get(shopify_handle = handle.upper().strip())
        print(Q, 'now going to add them to the database')
        sleep(4)
        for i in product['variants']:
            print(f'{i["id"]}  {i["title"]}', end='\t')
            try:
                QQ = Variant(product=Q, title=i['title'], price=float(i['price']), variant=i['sku']).save()

            except:
                print('ERROR OCCURER ^ - moving to next')

    except:
        print('FAILED - no product found / Error occured')

    print('\n DONE')
    pass





def barcode_reuse_1(VARIANT,PRICE,TITLE, COLOR, HANDLE, QUANTITY):
    TITLE = TITLE.split(' -[')[0]
    X = 1.25 * inch
    Y = 0.85 * inch
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=(X,Y))
    c.setTitle('BARCODE - Finger Lakes ReUse Inc.')
    #PRICE
    PRICE = f'${PRICE:.2f}'
    for i in range(QUANTITY):
        c.setFont("Helvetica-Bold", 16,)
        c.drawString(X*0.05,Y*0.72,f'{PRICE:>10}')
        #LINE
        c.line(X*0.2,Y*0.635,X*0.8,Y*0.635)
        #QR
        qr_code = qr.QrCode(VARIANT, height=X*0.43,width=X*0.43)
        qr_code.drawOn(c,X*0.0,Y*0.0)
        #TITLE
        if len(TITLE)<14:
            c.setFont("Helvetica-Bold", 8)
        else:
            c.setFont("Helvetica-Bold", 6)
        c.drawString(X*0.41, Y*0.45,f'{TITLE}')
        #COLOR
        c.setFont("Helvetica-Bold", 6)
        c.drawString(X*0.41,Y*0.275,f'{COLOR}')
        #HANDLE
        c.setFont("Helvetica", 6)
        c.drawString(X*0.41,Y*0.10,f'{HANDLE}')
        c.showPage()

    c.save()
    buffer.seek(0)
    return buffer


def color_wheel_2021(d=''):
    #INTENTIONALLY SETTING D TO BLANK, SINCE THIE DECLARATION HAPPENS ONE TIME! AND STATS THAT WAY TILL GUNICORN IS REBOOTED@!!!!!
    # NEVER KEEP PYTHONG FUNCTIONS WITH DEFAULT VALUES IN THE DECLATION SEGMENT.
    if d=='':
        d = datetime.now(tz=timezone('US/Eastern'))
    color_ref = datetime(2021,1,5, tzinfo=timezone('US/Eastern'))
    colors = ('B','Y','O','R','G','L' )
    return colors[ (d - color_ref).days // 7 % 6 ]


def color_wheel_2022(d=''):
    #INTENTIONALLY SETTING D TO BLANK, SINCE THIE DECLARATION HAPPENS ONE TIME! AND STATS THAT WAY TILL GUNICORN IS REBOOTED@!!!!!
    # NEVER KEEP PYTHONG FUNCTIONS WITH DEFAULT VALUES IN THE DECLATION SEGMENT.
    if d=='':
        d = datetime.now(tz=timezone('US/Eastern'))


    color_ref = datetime(2021,1,5, tzinfo=timezone('US/Eastern'))
    colors = ('B','Y','O','R','G','L' )



    current = (d - color_ref).days // 7 % 6

    return_dict = {
        'pricing': colors[current],
        'hold': colors[(current + 5) % 6],
        '25': colors[(current + 4) % 6],
        '50': colors[(current + 3) % 6],
        '75': colors[(current + 2) % 6],
        'reset': colors[(current + 1) % 6]
    }
    return return_dict




################### CAREFUL - - - - CHANGE using COMPARE_AT_PRICE REFERENCE
def drop_price(handle,factor, TAGS):   # SINGULAR HANDLE
    try:
        sleep(0.5)
        the_request = requests.get(S_URL+'products.json', params={'handle': handle, 'fields':'id,handle,variants'})
        the_response = json.loads(the_request.text)
    #     print('Query Shopify Response Code: ', the_request.status_code)
        sleep(0.5)
        the_id = the_response['products'][0]['id']

        update_dict = {'product': {'id':the_id, 'tags':TAGS } }
        update_variants = []
        for i in the_response['products'][0]['variants']:

                ######### IMPORTANT >>>>>>>>>> UPDATE WITH AI in COMPARE_AT_PRICE
            if float(factor)>=1.0:
                update_variants.append({'id':i['id'], 'price':  i['compare_at_price'] , 'compare_at_price': ''})
            elif type(i['compare_at_price']) == type(None):
                update_variants.append({'id':i['id'], 'price':  float(i['price'])*factor , 'compare_at_price': i['price']})
            else:
                update_variants.append({'id':i['id'], 'price': float( i['compare_at_price']) * factor , 'compare_at_price': i['compare_at_price']})


        update_dict['product']['variants'] = update_variants

        the_post = requests.put(S_URL + 'products/' + str(the_id) + '.json', json=update_dict)
        # print(handle," - UPDATE REQUEST Status Code (200 is good): ", the_post.status_code)
        # print(the_post.text)
        return the_post.status_code
    except:
        return '404'



def data1_handle_process(data1_handle):

    if data1_handle.strip() == '':
        return 'BLANK INPUT'

    price_progression = [1,2,3,4,5,6,7,8,9,10,  12,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,   150,175,200,225,250,275,300,325,350,375,400,425,450,475,500,525,550,575,600,625,650,675,700,725,750,775,800,825,850,875,900,925,950,975,  1000,1050,1100,1150,1200,1250,1300,1350,1400,1450,1500]
    color_lookup = {'W':'White','R':'Red','O':'Orange','G':'Green','B':'Blue','L':'Lavender','Y':'Yellow'}
    log = ''
    # 'first check if there exists the handle in the system:
    log += f'Attempting to check for input:[{data1_handle}] in data1 portal<br><br>'

    try:
        temp = Product.objects.get(shopify_handle=str(data1_handle),  )
        log += f'Product found in the system! Procuct(id): {temp.id} <br><br>'# Product.objects.get(shopify_handle='WTBKS')
        # CHECK ABOUT COLOR !!! > Only colors and White allowed
        if data1_handle[0].upper() in color_lookup:
            log += f'Color {color_lookup[ data1_handle[0] ]} <br><br>'
        else:
            log += f'Unsupported COLOR : {data1_handle[0]}. Only White/Green/Blue/Orange/Lavender/Yellow are allowed<br><br>'
            return log
        # CHECK IF THERE ARE NO VARIANTS IN THE CURRENT PRODUCT
        temp_length = len(Variant.objects.filter(product=temp))
        if temp_length <= 0:
            log += f'Verified OK:  There are variants under this product! <br><br>'
        else:
            log += f'FAILED!!:- Cannot generate variant to Products that have variants under them.<br><br>'
            log += f'There are {temp_length} variants under {data1_handle}<br><br>'
            log += f'There should 0 variants under this product in order to generate the standard items under it.'
            return log
    except:
        log += f'Product with specified handle was NOT found in the data1 Portal. (or other error occured when querying item)<br><br>'
        return log

    # ALL CHECKS PASSED AT THIS POINT > CREATE ITEMS
    log += f'... Now attempting to create variants in {data1_handle} between $1 and $1500<br><br>'

    try:
        for i in price_progression:
            Variant(  product=temp, title=f'${i}',  price=float(i), variant=f'{data1_handle}{i}'     ).save()
        log += '<strong>SUCCESS:</strong> VARIANTS CREATED SUCCESSFULLY! - Please verify them in the portal<br><br>'

    except:
        log += 'ERROR OCCURED - white generating products<br><br>'
        return log

    return log



def shopify_handle_process(shopify_handle):
    price_progression = [1,2,3,4,5,6,7,8,9,10,  12,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,   150,175,200,225,250,275,300,325,350,375,400,425,450,475,500,525,550,575,600,625,650,675,700,725,750,775,800,825,850,875,900,925,950,975,  1000,1050,1100,1150,1200,1250,1300,1350,1400,1450,1500]
    color_lookup = {'W':'White','R':'Red','O':'Orange','G':'Green','B':'Blue','L':'Lavender','Y':'Yellow'}
    log = ''

    if shopify_handle[0] not in color_lookup or len(shopify_handle)!=5:
        log += 'ERROR: Handle needs to be 5 character long AND the first character must be W/R/G/B/Y/O/L'
        return log

    #Contact Shopify

    log += f'Attempting to find [{shopify_handle}] in Shopify...<br><br>'
    sleep(1)
    the_request = requests.get(f'{S_URL}products.json?handle={shopify_handle}')
    the_response = the_request.json()

    if len(the_response['products']) == 0:
        log += f'FAIL: PRODUCT DOES NOT EXIST! - Please ensure the product exists<br><br>'
        return log
    elif len(the_response['products']) > 1:
        log += 'More than one product found, Not proceding'
        return log
    else: #MUST BE FOUND
        log += f'Handle FOUND: handle:[{shopify_handle}] exists in Shopify with ID:{the_response["products"][0]["id"]}<br><br>'

    variants_list = []
    for i in price_progression:
        variants_list.append({
            'option1':f'${i}',
            'price':i,
            'compare_at_price':'',
            'barcode': f'{shopify_handle}{i}',
            'sku': f'{shopify_handle}{i}',
            'inventory_managment':'shopify',
    })
    log += 'Attempting to add standard variants between $1-1500 in SHOPIFY<br><br>'

    try:
        sleep(2)
        the_post = requests.put(f'{S_URL}products/{the_response["products"][0]["id"]}.json',
            json = {
                'product':{
                    'id': the_response["products"][0]["id"],
                    'variants' : variants_list,
                    'tags': 'SRUE,data1-generator'

                }
        })
        log += f'Shopify Response Code : {the_post.status_code} [ FYI: 200=SUCCESS ]<br><br>'
        log += f'Please verify that the variants have been made!<br><br>'

        if the_post.status_code!=200:
            log += f'<br><br>Shopify Response:<br><br>{the_post.json()}'

    except:
        log += 'ERROR SUBMITTING SEQUENCE TO SHOPIFY'
        return log

    return log
