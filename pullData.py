import os
from datetime import datetime

designationToCloudiness = {
    "CLR" : 0.0,
    "FEW" : 2/8,
    "SCT" : 4/8, 
    "BKN" : 6/8,
    "OVC" : 1.0,
    "VV0" : 1.0
}

# Example data
# 24234KBFI BFI20180301000011603/01/18 00:00:31  5-MIN KBFI 010800Z 17008KT 10SM -RA OVC045 08/04 A2949 420 73 -200 160/08 RMK AO2 P0000 T00830039
#                             DATE     TIME                                          SKY CONDITION
# OVC045 means Overcast at a height of 4500 feet.
# OVC is a Okta measurement, to read into that you can read here: https://en.wikipedia.org/wiki/Okta
# To understand Sky condition, you can read the docs in td6401b.txt related to Sky Condition.
# 
# I'm abstracting Sky Condition into a float between 0 and 1
# Also I'm not positive that every 5 minute time period is represented.
# We can also pull 1 minute data frm here if needed ftp://ftp.ncdc.noaa.gov/pub/data/asos-onemin/

def extractFurthestSkyDesignation(items):
    # iterate backwards to find the last sky designation
    # The last sky designation is the furthest and will also be the most covering
    for item in items[::-1]:
        if len(item) >= 3:
            if item[0:3] in ["FEW", "CLR", "SCT", "BKN", "OVC", "VV0"]:
                return item[0:3]
    return None

def getTimeAndDesignation(line):
    items = line.split()
    date = items[1][-8:]
    time = items[2]
    timeOfOccurence = datetime.strptime(date + " " + time, '%m/%d/%y %H:%M:%S')
    designation = extractFurthestSkyDesignation(items)
    return (timeOfOccurence, designation)

def buildOrderedData(folderName):
    data = []
    lastDesignation = "CLR"
    for path in os.listdir(folderName):
        with open(os.path.join(folderName, path)) as fp:
            for line in fp:
                (timeOfOccurence, designation) = getTimeAndDesignation(line)
                if designation == None:
                    designation = lastDesignation
                cloudiness = designationToCloudiness[designation]
                data.append((timeOfOccurence, cloudiness))

                lastDesignation = designation
    # sort by time
    return sorted(data, key=lambda x: x[0])
