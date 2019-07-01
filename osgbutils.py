# osgbuils.py
# 
# Pyhon port of the Ordnance Survey SpreadSheet available at:
# https://www.ordnancesurvey.co.uk/docs/support/maptile-gridref-conversion.xls
#
# Created By: Dave Barrett
# Ceated On: 26/06/2019
import math
import re
gridLetters = {"SV":(0,0),"SQ":(0,1),"SL":(0,2),"SF":(0,3),"SA":(0,4),"NV":(0,5),"NQ":(0,6),"NL":(0,7),"NF":(0,8),"NA":(0,9),"HV":(0,10),"HQ":(0,11),"HL":(0,12),"SW":(1,0),
                "SR":(1,1),"SM":(1,2),"SG":(1,3),"SB":(1,4),"NW":(1,5),"NR":(1,6),"NM":(1,7),"NG":(1,8),"NB":(1,9),"HW":(1,10),"HR":(1,11),"HM":(1,12),
                "SX":(2,0),"SS":(2,1),"SN":(2,2),"SH":(2,3),"SC":(2,4),"NX":(2,5),"NS":(2,6),"NN":(2,7),"NH":(2,8),"NC":(2,9),"HX":(2,10),"HS":(2,11),"HN":(2,12),
                "SY":(3,0),"ST":(3,1),"SO":(3,2),"SJ":(3,3),"SD":(3,4),"NY":(3,5),"NT":(3,6),"NO":(3,7),"NJ":(3,8),"ND":(3,9),"HY":(3,10),"HT":(3,11),"HO":(3,12),
                "SZ":(4,0),"SU":(4,1),"SP":(4,2),"SK":(4,3),"SE":(4,4),"NZ":(4,5),"NU":(4,6),"NP":(4,7),"NK":(4,8),"NE":(4,9),"HZ":(4,10),"HU":(4,11),"HP":(4,12),
                "TV":(5,0),"TQ":(5,1),"TL":(5,2),"TF":(5,3),"TA":(5,4),"OV":(5,5),"OQ":(5,6),"OL":(5,7),"OF":(5,8),"OA":(5,9),"JV":(5,10),"JQ":(5,11),"JL":(5,12),
                "TW":(6,0),"TR":(6,1),"TM":(6,2),"TG":(6,3),"TB":(6,4),"OW":(6,5),"OR":(6,6),"OM":(6,7),"OG":(6,8),"OB":(6,9),"JW":(6,10),"JR":(6,11),"JM":(6,12)}

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
    letTuple = (math.floor(eastings/100000.0),math.floor(northings/100000.0))

    grid100km = [k for k,v in gridLetters.items() if v == letTuple][0]

    # convert the eastigns and northings to strings of legth 6 and 7
    if len(str(eastings)) <= 6:
        eastStr = str(eastings).zfill(6)
    else:
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
        
def gridCoords(reference):
    """Returns a tuple of (eastings, northings, squaresize) in metres from a full British National Grid Reference.
    
    reference can be in any of the following forms:

    SU
    SU03
    SU03NW
    SU0339
    SU0339NW
    SU031395
    SU03123956
    SU0312339567
    """
    
    # clean the input
    reference = reference.replace(" ","").upper()
    # grid quadrant included in the reference
    quadExists = False

    # define the patterns to match for each grid reference
    p0 = re.match('^[\\w]+$', reference) # checks that only alphanumeric chas are in the reference
    p1 = re.match('[HJNOST]{1}', reference[0]) # check the first 100km square is in HJNOST 
    p2 = re.match('[^I]{1}', reference[1]) # check the second char is not I
    p3 = re.match('[A-Z]{2}',reference[-2:]) # check if we have a quadrant reference
    p4 = re.match('[NS]{1}',reference[-2]) # check if quadrant first letter is valid
    p5 = re.match('[EW]{1}',reference[-1]) # check if quadrant second letter is valid


    # check validity of the supplied grid reference
    if p0 is None:
        return 'InvalidReferenceA'

    # check the 100km square validity and return the relevant coordinate tuple from gridLetters
    if p1 is None or p2 is None:
        return 'InvalidReferenceB'
    else:
        grid100km = gridLetters[reference[:2]]

    # check if we have a quadrant and if it is valid

    if p3 is None: 
        quadExists = False
    else:
        if p4 is None or p5 is None and len(reference) > 2: # need to include the length test to avoid returning invlaid for 100km ref only
            return 'InvalidReferenceC'
        else:
            quadExists = True
            quadLetters = reference[-2:]

    # retrieve the eastings and northings of the validated reference.
    if len(reference) == 2: # 100km grid
        eastings, northings = (n * 100000 for n in grid100km)
        squaresize = 100
        return eastings,northings,squaresize

    if len(reference) == 4: # 10km grid
        eastings = int(str(grid100km[0]) + reference[2]) * 10000
        northings = int(str(grid100km[1]) + reference[3]) * 10000
        squaresize = 10
        return eastings,northings,squaresize
    
    if len(reference) == 6: # 5km or 1km grid
        if quadExists:
            if quadLetters == 'NW':
                quadDigit = ('0','5')
            elif quadLetters == 'NE':
                quadDigit = ('5','5')
            elif quadLetters == 'SW':
                quadDigit('0','0')
            elif quadLetters == 'SE':
                quadDigit = ('5','0')
            eastings = int(str(grid100km[0]) + reference[2] + quadDigit[0]) * 1000
            northings = int(str(grid100km[1]) + reference[3] + quadDigit[1]) * 1000
            squaresize = 5
        else:
            eastings = int(str(grid100km[0]) + reference[2:4]) * 1000
            northings = int(str(grid100km[1]) + reference[4:]) * 1000
            squaresize = 1 
        return eastings,northings,squaresize

    if len(reference) == 8: # 500m or 100m grid
        if quadExists:
            if quadLetters == 'NW':
                quadDigit = ('0','5')
            elif quadLetters == 'NE':
                quadDigit = ('5','5')
            elif quadLetters == 'SW':
                quadDigit('0','0')
            elif quadLetters == 'SE':
                quadDigit = ('5','0')
            eastings = int(str(grid100km[0]) + reference[2:4] + quadDigit[0]) * 100
            northings = int(str(grid100km[1]) + reference[4:6] + quadDigit[1]) * 100
            squaresize = 0.5
        else:
            eastings = int(str(grid100km[0]) + reference[2:5]) * 100
            northings = int(str(grid100km[1]) + reference[5:]) * 100
            squaresize = 0.1 
        return eastings,northings,squaresize

    if len(reference) == 10: # 10m grid
        eastings = int(str(grid100km[0]) + reference[2:6]) * 10
        northings = int(str(grid100km[1]) + reference[6:]) * 10
        squaresize = 0.01
        return eastings,northings,squaresize  
      
    if len(reference) == 12: # 1m grid
        eastings = int(str(grid100km[0]) + reference[2:7])
        northings = int(str(grid100km[1]) + reference[7:])
        squaresize = 0.001
        return eastings,northings,squaresize

if __name__ == '__main__':
    print(gridLetters["SU"])
    letters = [k for k,v in gridLetters.items() if v == (4,1)]
    print (letters)
    print (gridSquare(15000,439500,0.1))
    print (gridCoords('se0339nw'))
