from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
# Create your views here.

from qbgiftcard.models import GiftCard

from qbgiftcard.models import *

from json import dumps

from datetime import datetime, timedelta
import pytz

from django.db.models.functions import Trunc







def qbgiftcardhome(request):
    G = GiftCard.objects.all()
    customer_dict = []
    for i in G:
        customer_dict.append([i.id, i.first_name, i.last_name, i.phone, i.email ])
    return render(request, 'qbgiftcard/default1.html', {'customer_dict': dumps(customer_dict)})


def lookup(request):
    if not request.user.is_authenticated:
        return redirect('HOME')
    try:
        x = int(request.POST['customer_id'])
        g = GiftCard.objects.get(id=x)
        staff_id = str(request.user.email).split('@fingerlakesreuse.org')[0]
        AccessLog.objects.create(staff_id=staff_id, giftcard=g)
    except:
        return HttpResponse('<h1>error occured</h1>')
    return redirect('qbgiftcard:results')




def results(request):
    if not request.user.is_authenticated:
        return redirect('HOME')
    try:
        staff_id = str(request.user.email).split('@fingerlakesreuse.org')[0]
        last_record = AccessLog.objects.filter(staff_id=staff_id).order_by('-timestamp')[0]
        gift_card_record = GiftCard.objects.get(id=last_record.giftcard_id)
        gift_card_code = gift_card_record.giftcard.replace(' ','')
        gift_card_name = f'{gift_card_record.last_name}, {gift_card_record.first_name}'



        access_log = AccessLog.objects.filter(giftcard_id=last_record.giftcard_id).order_by('-timestamp')[:100]\
            .annotate(DATE_TIME = Trunc('timestamp', kind='second', tzinfo=pytz.timezone('US/Eastern')))\
            .values('DATE_TIME','staff_id')

        for i in access_log:
            i['DATE_TIME'] = datetime.strftime(i['DATE_TIME'],'%b %d, %Y - %I:%M %p')

    except:
        print('ERROR')
        pass
    return render(request, 'qbgiftcard/lookup1.html', {'gift_card_code': gift_card_code, 'gift_card_name': gift_card_name, 'access_log':access_log})
