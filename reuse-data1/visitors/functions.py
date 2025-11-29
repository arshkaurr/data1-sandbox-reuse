

from datetime import datetime
import pytz
#  CONVERTS ANY DATETIME OBJCECT TO US/EASTERN TIME
def useastern(any_timestamp=''):
    if any_timestamp == '' :
        return datetime.now().astimezone(pytz.timezone('US/Eastern'))
    return any_timestamp.astimezone(pytz.timezone('US/Eastern'))

def useastern_start(any_timestamp=''):
    if any_timestamp == '' :
        return datetime.now().astimezone(pytz.timezone('US/Eastern')).replace(hour=0,minute=0,second=0,microsecond=0)
    return any_timestamp.astimezone(pytz.timezone('US/Eastern')).replace(hour=0,minute=0,second=0,microsecond=0)

def useastern_end(any_timestamp=''):
    if any_timestamp == '' :
        return datetime.now().astimezone(pytz.timezone('US/Eastern')).replace(hour=23,minute=59,second=59,microsecond=999999)
    return any_timestamp.astimezone(pytz.timezone('US/Eastern')).replace(hour=23,minute=59,second=59,microsecond=999999)






##############################################################
#  function;   Default is month!!!!!!!!!!!!
# The function takes in the request.GET object and tries to make get the start and end date
#

#Input is the request.GET object

def start_end_date(GET, type='month'):
    try:
        temp_date = datetime.strptime(GET['start'],'%Y-%m-%d')
        start_date = datetime.now(pytz.timezone('US/Eastern')).replace(year=temp_date.year,month=temp_date.month,day=temp_date.day)
    except:
        start_date = datetime.now(pytz.timezone('US/Eastern')).replace(day=1)
    finally:
        temp_date = None

    try:
        temp_date = datetime.strptime(GET['end'],'%Y-%m-%d')
        end_date = datetime.now(pytz.timezone('US/Eastern')).replace(year=temp_date.year,month=temp_date.month,day=temp_date.day)
    except:
        end_date = datetime.now(pytz.timezone('US/Eastern'))

    if end_date < start_date:
        start_date, end_date = end_date, start_date


    start_date = start_date.replace(hour=0,minute=0,second=0,microsecond=0)
    end_date = end_date.replace(hour=23,minute=59,second=59,microsecond=999999)


    return start_date, end_date




#####################################################
# Function to get simulated Capacity of a Visitors OBject and Write its 'capcity' field to the running total of the day / Capacity of it locations
#####################################################
from visitors.models import Visitors
from django.db.models import Sum

def capacity_generate(x):

    capacities = {'IRC':140,'TRC':183,'RCH':175, '700-CABOOSE':35, '700-WAREHOUSE': 38, 'TEST':999, 'DDO':999, '700RNR': 35, 'TRC-DONATIONS': 999}

    QUERY = Visitors.objects.filter(location=x.location, timestamp__range=(useastern_start(x.timestamp), useastern(x.timestamp))).aggregate(Running_total=Sum('count'))
    x.capacity = QUERY['Running_total'] / capacities[x.location]
    x.save()
    return x.capacity
