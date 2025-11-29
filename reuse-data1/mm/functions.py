from bitcoin import sha256
import json

#-----------------START EXPANSION FUNCTION

def ExpansionFunction(mFormData):

    ExpansionDict = {
        'eName' : mFormData['rName'],
        'eDate' : mFormData['rDate'],
        'eMode' : mFormData['rMode'],
        'eTrips' : mFormData['rTrips'],
        'eOrigin' : mFormData['rOrigin'],
        'eOriginLocation' : mFormData['rOriginLocation'],
        'eDestination' : mFormData['rDestination'],
        'eDestinationLocation' : mFormData['rDestinationLocation'],
        'eTimestamp' : mFormData['rTimestamp'],
        }

    #EXPANSION
    #STEP 1 : Compress the data if there are repeats
    # AND Make a new DICT with common items
    RawMaterialObject = json.loads(mFormData['rMaterial'])
    RawMaterialDict = {}

    for row,item in enumerate(RawMaterialObject):
        if RawMaterialObject[row][0] not in RawMaterialDict:
            RawMaterialDict[RawMaterialObject[row][0]] = float(RawMaterialObject[row][1])
        else:
            RawMaterialDict[RawMaterialObject[row][0]] += float(RawMaterialObject[row][1])

    #STEP 2 : ZIP
    FinalMaterialRecords = []
    if mFormData['rMode'].strip().lower() == 'forklift':
        #START EXPANSION FUNCTION
        #Prepre the EXPANSIONLIST - a list with TUPLES
        RawMaterialList = []
        for item in RawMaterialDict:
            for i in range(0,int(RawMaterialDict[item])):
                RawMaterialList.append((item,1))
            if RawMaterialDict[item]%1 != 0:
                RawMaterialList.append((item,RawMaterialDict[item]%1))

        # EACH INDIVIDUAL Pallet GETS the SAME TripID (HASH)
        for (i,(material,pallets)) in enumerate(RawMaterialList):
            tempdict = ExpansionDict.copy()
            tempdict['eMaterial'] = material
            tempdict['ePallets'] = pallets
            tempdict['eTripID'] = sha256(str(tempdict['eTimestamp']) + '-' + str(i))
            FinalMaterialRecords.append(tempdict)

        MESSAGE = FinalMaterialRecords
        # _END EXPANSION FUNCTIONS


    elif mFormData['rMode'].strip().lower() == 'truck':
        # EACH MATERIAL GETS the SAME TripID (HASH)
        #START FUNCTION CONVERSION
        for item in RawMaterialDict:
            tempdict = ExpansionDict.copy()
            tempdict['eMaterial'] = item
            tempdict['ePallets'] = RawMaterialDict[item]
            tempdict['eTripID'] = sha256(str(tempdict['eTimestamp']))
            FinalMaterialRecords.append(tempdict)
        MESSAGE = FinalMaterialRecords
        #END FUNCTION CONVERSION



    elif mFormData['rMode'].strip().lower() == 'manual':
        if mFormData['rTrips'] == 'one':
            # EACH MATERIAL GETS the SAME TripID (HASH)
            #START FUNCTION CONVERSION
            for item in RawMaterialDict:
                tempdict = ExpansionDict.copy()
                tempdict['eMaterial'] = item
                tempdict['ePallets'] = RawMaterialDict[item]
                tempdict['eTripID'] = sha256(str(tempdict['eTimestamp']))
                FinalMaterialRecords.append(tempdict)
            MESSAGE = FinalMaterialRecords
            #END FUNCTION CONVERSION
        elif mFormData['rTrips'] == 'multiple':
            #START EXPANSION FUNCTION
            #Prepre the EXPANSIONLIST - a list with TUPLES
            RawMaterialList = []
            for item in RawMaterialDict:
                for i in range(0,int(RawMaterialDict[item])):
                    RawMaterialList.append((item,1))
                if RawMaterialDict[item]%1 != 0:
                    RawMaterialList.append((item,RawMaterialDict[item]%1))

            # EACH INDIVIDUAL Pallet GETS the SAME TripID (HASH)
            for (i,(material,pallets)) in enumerate(RawMaterialList):
                tempdict = ExpansionDict.copy()
                tempdict['eMaterial'] = material
                tempdict['ePallets'] = pallets
                tempdict['eTripID'] = sha256(str(tempdict['eTimestamp']) + '-' + str(i))
                FinalMaterialRecords.append(tempdict)

            MESSAGE = FinalMaterialRecords
            # _END EXPANSION FUNCTIONS



        #START EXPANSION FUNCTION
        #Prepre the EXPANSIONLIST - a list with TUPLES

        # RawMaterialList = []
        # for item in RawMaterialDict:
        #     for i in range(0,int(RawMaterialDict[item])):
        #         RawMaterialList.append((item,1))
        #     if RawMaterialDict[item]%1 != 0:
        #         RawMaterialList.append((item,RawMaterialDict[item]%1))
        #
        # # EACH INDIVIDUAL Pallet GETS the SAME TripID (HASH)
        # for (i,(material,pallets)) in enumerate(RawMaterialList):
        #     tempdict = ExpansionDict.copy()
        #     tempdict['eMaterial'] = material
        #     tempdict['ePallets'] = pallets
        #     tempdict['eTripID'] = sha256(str(tempdict['eTimestamp']) + '-' + str(i))
        #     FinalMaterialRecords.append(tempdict)
        #
        # MESSAGE = FinalMaterialRecords

        # _END EXPANSION FUNCTIONS



    else:
        MESSAGE = 'ERROR - NOT DETECTED'

    return MESSAGE
#-----------------END EXPANSION FUNCTION





def AddAll():
    from mm.models import RawMaterialMovement, ExpandedMaterialMovement
    ExpandedMaterialMovement.objects.all().delete()
    for i in RawMaterialMovement.objects.all():
        if str(i.__all__()['rHidden']).strip().lower() != 'test':
            for j in ExpansionFunction(i.__all__()):
                ExpandedMaterialMovement.objects.create(**j).save()


def RebuildMM():
    import os
    import json
    from mm.models import RawMaterialMovement
    from mm.functions import AddAll

    text_records = os.listdir('raw_log')

    RawMaterialMovement.objects.all().delete()

    for i in text_records:
        with open('raw_log/' + i) as temp:
            RawMaterialMovement.objects.create(**(json.loads(temp.read())))

    AddAll()



def expand_locations_in_order(query, classifier):
    ############### HARDCODED LOCATION LIST I,T,7
    return_dict = {'IRC': 0.0, 'TRMC': 0.0, '700': 0.0, 'D': 0.0}
    return_map = {'I':'IRC', 'T': 'TRMC', '7': '700', 'D': 'DOT'}
    query_zip = dict()
    for i in query:
        query_zip[return_map[i[classifier]]] = i['Pallets']

    for i in query_zip:
        return_dict[i] = query_zip[i]

    print(return_dict)
    return return_dict
