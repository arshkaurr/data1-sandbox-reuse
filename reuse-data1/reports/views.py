from django.shortcuts import render
from django.http import HttpResponse

from mm.models import ExpandedMaterialMovement
from django.db.models import Sum

from datetime import datetime

# Create your views here.
def materialflow(request):

#####################################################################################################
    ###Step 1 : Determine if the Date values are valid and acceptable. (Swap them if mixed in range)
    flag = False
    if 'start' in request.GET and 'end' in request.GET:
        if request.GET['start'] != '' and request.GET['end'] != '':
            try:
                start_date = datetime.strptime(request.GET['start'], '%Y-%m-%d')
                end_date = datetime.strptime(request.GET['end'], '%Y-%m-%d')
                flag = True
                if start_date > end_date:
                        start_date, end_date = end_date , start_date
            except:
                pass

    ###Step 2 : If they are valid then pass them to the list, if not generate default starting from this month
    if not flag:
        start_date=datetime.now().replace(day=1)
        end_date = datetime.now()

    ### Step 3 : Crunch the start_date and end_date to strings for Django Date Range + html output
    start_date = datetime.strftime(start_date,'%Y-%m-%d')
    end_date = datetime.strftime(end_date,'%Y-%m-%d')
#####################################################################################################

    e = ExpandedMaterialMovement.objects.filter(eDate__range=[start_date,end_date])
    print(len(e))

    return render(request,'reports/materialflow.html', {
    'start_date' : start_date,
    'end_date' : end_date,
    'total_pallets' : e.filter(eOrigin='donations').aggregate(Sum('ePallets'))['ePallets__sum'],
    'total_to_processing' : e.filter(eOrigin='donations',eDestination='processing').aggregate(Sum('ePallets'))['ePallets__sum'],
    'total_to_overflow' : e.filter(eOrigin='donations', eDestination='overflow').aggregate(Sum('ePallets'))['ePallets__sum'],

    'processing_from_ddo' : e.filter(eOrigin='donations', eDestination='processing').aggregate(Sum('ePallets'))['ePallets__sum'],
    'processing_from_overflow' : e.filter(eOrigin='overflow', eDestination='processing').aggregate(Sum('ePallets'))['ePallets__sum'],
    'processing_to_irc' : e.filter(eDestination='processing',eDestinationLocation='IRC').aggregate(Sum('ePallets'))['ePallets__sum'],
    'processing_to_trc' : e.filter(eDestination='processing',eDestinationLocation='TRC').aggregate(Sum('ePallets'))['ePallets__sum'],
    })
