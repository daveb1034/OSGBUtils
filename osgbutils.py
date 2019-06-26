# osgbuils.py
# 
# Pyhon port of the Ordnance Survey SpreadSheet available at:
# https://www.ordnancesurvey.co.uk/docs/support/maptile-gridref-conversion.xls
#
# Created By: Dave Barrett
# Ceated On: 26/06/2019

#gridLetters = {"SV":(0,0),"SQ":(0,1),"SL":(0,2),"SF":(0,3),"SA":(0,4),"NV":(0,5),"NQ":(0,6),"NL":(0,7),"NF":(0,8),"NA":(0,9),"HV":(0,10),"HQ":(0,11),"HL":(0,12),
#                "SW":(1,0),"SR":(1,1),"SM":(1,2),"SG":(1,3),"SB":(1,4),"NW":(1,5),"NR":(1,6),"NM":(1,7),"NG":(1,8),"NB":(),"HW":(),"HR":(),"HM":()}

def gridLetters(e, n):
    """Return full 6 Figure OS Grid Reference in the form SU 499 729."""

    import math
    # List of available grid letters, I is not included
    gridChars = "ABCDEFGHJKLMNOPQRSTUVWXYZ"

    # need to make sure e / n wihin range
    
    # get the 100km grid indices
    e100k = math.floor(e/100000)
    n100k = math.floor(n/100000)

    # translate to numeric equivalent of the grid letters
    l1 = (19-n100k)-(19-n100k)%5+math.floor((e100k+10)/5)
    l2 = (19-n100k)*5%25 + e100k%5

    letPair = gridChars[int(l1)] + gridChars[int(l2)]
    return letPair

if __name__ == '__main__':
    print(gridLetters(00000,1200000))