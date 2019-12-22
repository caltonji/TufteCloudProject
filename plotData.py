import os
from datetime import datetime
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

np.random.rand(10, 12)
xPadding = 20
yPadding = 20
dayWidth = 2
# width = 10000
height = 500

designationMap = {
    "CLR" : 0.0,
    "FEW" : 2/8,
    "SCT" : 4/8, 
    "BKN" : 6/8,
    "OVC" : 1.0,
    "VV0" : 1.0
}

def extractLastSkyDesignation(items):
    for item in items[::-1]:
        if len(item) >= 3:
            if item[0:3] in ["FEW", "CLR", "SCT", "BKN", "OVC", "VV0"]:
                return item[0:3]
    return None

def getAmountOfDesignation(desigation):
    return designationMap[desigation]

def averagePoints(data):
    total = 0.0
    for dataPoint in data:
        total += getAmountOfDesignation(dataPoint[1])
    return total / len(data)

def buildOrderedData(folderName):
    data = []
    lastDesignation = "CLR"
    for path in os.listdir(folderName):
        with open(os.path.join(folderName, path)) as fp:
            for line in fp:
                items = line.split()
                # print(items)
                date = items[1][-8:]
                time = items[2]
                timeOfOccurence = datetime.strptime(date + " " + time, '%m/%d/%y %H:%M:%S')
                designation = extractLastSkyDesignation(items)
                if designation == None:
                    designation = lastDesignation
                cloudiness = getAmountOfDesignation(designation)
                data.append((timeOfOccurence, cloudiness))

                lastDesignation = designation
    data = sorted(data, key=lambda x: x[0])
    return np.array(data)

if __name__ == "__main__":
    weatherData = buildOrderedData("./boeing2018")
    
    framedData = []
    for item in weatherData:
        dt = item[0]
        framedData.append((dt.timetuple().tm_yday, dt.hour * 60 + dt.minute, item[1]))

    df = pd.DataFrame(framedData, columns=["day", "minute", "opacity"])
    df = df.pivot_table(index='day', columns='minute', values='opacity')
    # im = Image.new('RGBA', (width, height))
    # draw = ImageDraw.Draw(im)
    # # draw.rectangle([(0, 0), (width, height)], fill=(0, 0, 0, 255))

    # for i in range(0, len(weatherData), countToAverageOn):
    #     opacity = averagePoints(weatherData[i:i+countToAverageOn])
    #     draw.line([(i/countToAverageOn,0),(i/countToAverageOn,height)], fill=(0,0,0, int(255 * opacity)), width=1)
    # im.show()
    print(df)
    print(type(df).__name__)
    ax = sns.heatmap(df)
    plt.show()
