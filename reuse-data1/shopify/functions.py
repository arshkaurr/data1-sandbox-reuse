from local_settings import S_URL

import requests
from bs4 import BeautifulSoup
import json
import re
from time import sleep
from datetime import datetime


#ReportLab
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
import io






#######################################################################################################
#SURE FUNCTION - Definitely returns something
#Function will raise an error for invalid code or inability to get sucessful parameters
def acetap_function(code):
    request = requests.get(f'https://www.acehardware.com/search?searchSettings=lowerMatch&query={code}')
    request.encoding = 'utf-8'
    if request.status_code!=200  or  request.url.strip()[:40]!='https://www.acehardware.com/departments/':
        raise NameError
    else:
        data = json.loads(re.findall(r'<script type="text/json" id="data-mz-preload-product">(.*?)</script>',request.text)[0])
        soup = BeautifulSoup(request.text,'html.parser')

        #COMPLIE THE SALE AND REGULAR PRICE
        if data['price']['onSale'] == True:
            saleprice = data['price']['salePrice']
        else:
            saleprice = data['price']['price']

        #COMPILE THE SPECS, FEATURES, ETC.
        features = []
        specifications = {}
        producttype = ''
        whatsinthebox = ''
        try:
            for i in data['properties']:
                if not i['isHidden']:
                    if 'stringValue' in i['values'][0]:
                        if 'tenant~feature-' in i['attributeFQN']:
                            features.append(i['values'][0]['stringValue'])
                        if 'tenant~whats-in-the-box' in i['attributeFQN']:
                            whatsinthebox = i['values'][0]['stringValue']
                        if 'tenant~A0' in i['attributeFQN']:
                            specifications[i['attributeDetail']['name']] = i['values'][0]['stringValue']
                        if 'tenant~product-type' in i['attributeFQN']:
                            producttype = i['values'][0]['stringValue']
        except:
            pass


        return {
            'url': request.url,
            'code' : code,
            'title': data['content']['productName'].strip(),
            'mpn': data['mfgPartNumber'].strip(),
            'description' : data['content']['productFullDescription'].strip(),
            'category1': request.url[40:].split('/')[0],
            'category2': request.url[40:].split('/')[1],
            'category3': request.url[40:].split('/')[2],
            'photos':  ['https:' + i['src'] for i in data['content']['productImages']],

            'price': data['price']['price'],
            'saleprice': saleprice,

            'producttype': producttype,
            'whatsinthebox' : whatsinthebox,
            'features': features,
            'specifications': specifications,

        }


#######################################################################################################
# TESTER FUNCTION - THIS IS USE FOR PRE-TESTING and DEPLOYMENT OF A FUNCTION
# UNSURE FUNCTION  - ERROR AT ANY FAIL
# MULTIPLE REQUETST!!!!
def shopify_get_query(endpoint_url='',params={}, endpoint=''):
    the_request_url = S_URL + endpoint_url
    the_request = requests.get(the_request_url,params=params)
    return_list = json.loads(the_request.text)[endpoint]

    while('next' in the_request.links):
        the_request_url = the_request.links['next']['url']
        ####### NOTE !!!!!!!!! - HARDCODED API VERSION NUMBER - NOW 2020/>>>>>07<<<<<<<
        the_request_url = the_request_url.replace('https://fingerlakesreuse.myshopify.com/admin/api/2021-01/',S_URL)
        print('\n\nBEFORE',the_request.links,'\n')
        the_request = requests.get(the_request_url)
        print('\n\nAFTER',the_request.links,'\n\n\n')
        return_list += json.loads(the_request.text)[endpoint]
        sleep(4)

    # if 'Link' in the_request.headers:
    #     print('\n\n',the_request.links,'\n\n')
    print("DONE \n DONE \n DONE \n DONE")   #TTTTTTTTTTTTTTTTTTTTTTTTTTT
    return return_list


#######################################################################

def FINAL_import():
    import pandas as pd
    from shopify.models import AceInventoryList
    FINAL = pd.read_csv('FINAL.csv')
#    AceInventory.objects.all().delete()
    for i in range(FINAL.shape[0]):
        FINAL_dict = {
            'Index' : i,
            'ItemCode' : FINAL.loc[i]['SKU'],
            'Location' : FINAL.loc[i]['Loc'],
            'Department' : FINAL.loc[i]['Dept #'],
            'Title' : FINAL.loc[i]['Description'],
            'Upc' : FINAL.loc[i]['UPC'],
            'Qoh' : FINAL.loc[i]['QOH'],
            'Mpn' : FINAL.loc[i]['Mfg Part #'],
            'Retail' : FINAL.loc[i]['Retail'],
            'Status' : FINAL.loc[i]['STATUS'],
        }
        AceInventoryList.objects.create(**FINAL_dict).save()
        print(FINAL_dict)


############################################################################
#THIS IS SPECIFIC TO POSTIN THE ITEMS IN QUEUE
# WARNING:  THIS FUNCTION DOESN'T CHECK IF THE PRODUCT IS IN shopify
# IT ONLY CHECKS FOR STATUS- and POSTS REGARDLESS

def rch_post_shopify(itemindex):
    from local_settings import S_URL
    from shopify.models import AceInventoryList

    try:
        query = AceInventoryList.objects.get(Index=itemindex)
        if query.Status == 'QUEUED' or query.Status == 'zero':
            PRODUCT = {'product':
            {
            'title': str(query.Title),
            'handle' : str(query.ItemCode),
            'product_type': 'R-' + str(query.Department),
            'published': 'FALSE',
            'vendor': 'RCH-ACE',
            'variants': [{
                'sku':'R-' + str(query.Location) + '-' + str(query.ItemCode),
                'compare_at_price': str(query.Retail),
                # DROP PRICE DISCOUNT HERE FOR NEW PRODUCTS (NOW 75% OFF - 2021)
                'price': f'{float(query.Retail) * 0.75:.2f}',
                'barcode': query.Upc,
                'inventory_quantity': query.Qoh,
                'inventory_management': 'shopify',
                }]
            }}
            request = requests.post(S_URL+'products.json', json=PRODUCT)
            if request.status_code!=201 and request.status_code!=200:
                raise ImportError
            else:
                query.save()
                return True
        else:
            raise NameError
    except:
        return False







##################################################
#BARCODE FUNCTION - IN TEST MODE
def rch_barcode_generator(PRICE,BARCODE,TITLE,QUANTITY):
    X = 1.25 * 300
    Y = 0.85 * 300
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=(X,Y))

    for i in range(QUANTITY):
        c.setFont("Helvetica", 5)
        c.line(0,Y*0.75,X,Y*0.75)
        x = code128.Code128(BARCODE,barWidth=3.33, barHeight=65).drawOn(c,25,38)
        c.setTitle('BARCODE')
        c.setFont("Helvetica-Bold", 60)
        c.drawString(55,125,f'{PRICE:>8}')
        c.setFont("Helvetica", 30)
        c.drawString(28,Y*0.80,f'{TITLE:>20}')
        c.showPage()
    #End part to close the PDF
    c.save()
    buffer.seek(0)
    return buffer





from django.utils import timezone
#################### IMPORTER FUNCTION SETUP!!!!! ########################
################## SETUP THE BASE BARCODES IN THE SYSTEM TO MONITOR
##########################################################################
# the ITEM CODES HAVE BEEN HARDCODED TEMPORARILY,  In future they will be store in a model/the DB
def build_barcode_inventory_ids():#Function returns a dictionry which have {'barcode':'inventory_id',...}
    #list of inventory items to track
    LIST = ['99900000','99800000','99700000','99600000',  '99400000','99000000','99500000','99300000','99200000','99100000','98900000',     '98800000','98600000']
    request = requests.get(S_URL+'/products.json',params={'handle':','.join(LIST),'fields':'id,variants,handle,title,product_type,vendor,body_html'})
    response = json.loads(request.text)
    barcode_db = []
    for VARIANTS in response['products']:
        for VARIANT in VARIANTS['variants']:
            temp_dict = {
            'timestamp' : timezone.now(),
            'handle' : VARIANTS['handle'],
            'barcode' : VARIANT['barcode'],
            'title' : VARIANTS['title'],
            'option1' : VARIANT['option1'],
            'product_id' : VARIANT['product_id'],
            'variant_id' : VARIANT['id'],
            'compare_at_price' : float(VARIANT['compare_at_price']),
            'inventory_item_id' : VARIANT['inventory_item_id'],
            'product_type' : VARIANTS['product_type'],
            'vendor': VARIANTS['vendor'],
            'sku' : VARIANT['sku'],
            'body_html' : ' ' #VARIANTS['body_html'] ############### OVERIDIE TO NULL FOR NOW
            }
            barcode_db.append(temp_dict)
    #Print out a list of Handles in the set
    print(LIST,'\n\n\n\nHandles in the response:')
    for PRODUCTS in response['products']:
        print(PRODUCTS['handle'])

    return barcode_db
############################ IMPORTANTTTTTTTTTTTTTTTTTTTTTTTTTTT ****############

#YOU NEED TO MANUALLY PUBLISH CHANGES TO THE DATABASE !!!!!!!!!!!!!!!
#THIS FUNCTION DOES PUBLISH CHANGES

##########################################################################
