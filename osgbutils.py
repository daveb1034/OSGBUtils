# osgbuils.py
# 
# Pyhon port of the Ordnance Survey SpreadSheet available at:
# https://www.ordnancesurvey.co.uk/docs/support/maptile-gridref-conversion.xls
#
# Created By: Dave Barrett
# Ceated On: 26/06/2019
import math
gridLetters = {"SV":(0,0),"SQ":(0,1),"SL":(0,2),"SF":(0,3),"SA":(0,4),"NV":(0,5),"NQ":(0,6),"NL":(0,7),"NF":(0,8),"NA":(0,9),"HV":(0,10),"HQ":(0,11),"HL":(0,12),"SW":(1,0),
                "SR":(1,1),"SM":(1,2),"SG":(1,3),"SB":(1,4),"NW":(1,5),"NR":(1,6),"NM":(1,7),"NG":(1,8),"NB":(1,9),"HW":(1,10),"HR":(1,11),"HM":(1,12),
                "SX":(2,0),"SS":(2,1),"SN":(2,2),"SH":(2,3),"SC":(2,4),"NX":(2,5),"NS":(2,6),"NN":(2,7),"NH":(2,8),"NC":(2,9),"HX":(2,10),"HS":(2,11),"HN":(2,12),
                "SY":(3,0),"ST":(3,1),"SO":(3,2),"SJ":(3,3),"SD":(3,4),"NY":(3,5),"NT":(3,6),"NO":(3,7),"NJ":(3,8),"ND":(3,9),"HY":(3,10),"HT":(3,11),"HO":(3,12),
                "SZ":(4,0),"SU":(4,1),"SP":(4,2),"SK":(4,3),"SE":(4,4),"NZ":(4,5),"NU":(4,6),"NP":(4,7),"NK":(4,8),"NE":(4,9),"HZ":(4,10),"HU":(4,11),"HP":(4,12),
                "TV":(5,0),"TQ":(5,1),"TL":(5,2),"TF":(5,3),"TA":(5,4),"OV":(5,5),"OQ":(5,6),"OL":(5,7),"OF":(5,8),"OA":(5,9),"JV":(5,10),"JQ":(5,11),"JL":(5,12),
                "TW":(6,0),"TR":(6,1),"TM":(6,2),"TG":(6,3),"TB":(6,4),"OW":(6,5),"OR":(6,6),"OM":(6,7),"OG":(6,8),"OB":(6,9),"JR":(6,11),"JM":(6,12)}

def gridSquare(eastings, northings, squaresize):
    """Returns the appropriate National Grid Reference including 100km letters.

    eastings: in metres between 0 and 700000
    northings: in metres between 0 and 1300000
    squaresize: in kilometres, valid values are 100,10,5,1,0.5,0.1,0.01,0.001
    """

    # check inputs are valid
    if eastings < 0 or eastings >= 700000:
        return 'InvalidEastings'
    if northings < 0 or northings >= 1300000:
        return 'InvalidNorthings'
    if not squaresize in [100,10,5,1,0.5,0.1,0.01,0.001]:
        return 'InvalidSqaureSize'
    
    # get the 100km eastings and northings tuple
    letTuple = (math.floor(eastings/100000),math.floor(northings/100000))

    grid100km = [k for k,v in gridLetters.items() if v == letTuple][0]

    # convert the eastigns and northings to strings of legth 6 and 7
    eastStr = str(eastings)

    if len(str(northings)) <= 7:
        northStr = str(northings).zfill(7)
    else:
        northStr = str(northings)
    
    # extract out the grids to the required sqaure size
    if squaresize == 100:
        return grid100km
    elif squaresize == 10:
        return grid100km + eastStr[1] + northStr[2:3]
    elif squaresize == 5:
        if int(eastStr[2]) < 5 and int(northStr[3]) < 5:
            return grid100km + eastStr[1] + northStr[2:3] + 'SW'
        elif int(eastStr[2]) < 5 and int(northStr[3]) >= 5:
            return grid100km + eastStr[1] + northStr[2:3] + 'NW'
        elif int(eastStr[2]) >= 5 and int(northStr[3]) < 5:
            return grid100km + eastStr[1] + northStr[2:3] + 'SE'
        elif int(eastStr[2]) >= 5 and int(northStr[3]) >= 5:
            return grid100km + eastStr[1] + northStr[2:3] + 'NE'
    elif squaresize == 1:
        return grid100km + eastStr[1:3] + northStr[2:4]
    elif squaresize == 0.5:
        if int(eastStr[3]) < 5 and int(northStr[4]) < 5:
            return grid100km + eastStr[1:3] + northStr[2:4] + 'SW'
        elif int(eastStr[3]) < 5 and int(northStr[4]) >= 5:
            return grid100km + eastStr[1:3] + northStr[2:4] + 'NW'
        elif int(eastStr[3]) >= 5 and int(northStr[4]) < 5:
            return grid100km + eastStr[1:3] + northStr[2:4] + 'SE'
        elif int(eastStr[3]) >= 5 and int(northStr[4]) >= 5:
            return grid100km + eastStr[1:3] + northStr[2:4] + 'NE'
    elif squaresize == 0.1:
        return grid100km + eastStr[1:4] + northStr[2:5]
    elif squaresize == 0.01:
        return grid100km + eastStr[1:5] + northStr[2:6]
    elif squaresize == 0.001:
        return grid100km + eastStr[1:] + northStr[2:]
        

    

if __name__ == '__main__':
    print(gridLetters["SU"])
    letters = [k for k,v in gridLetters.items() if v == (4,1)]
    print (letters)
    print (gridSquare(125556,125456,0.001))
