from pullData import buildOrderedData
from PIL import Image, ImageDraw

countToAverageOn = 12
width = int(365 * 24 * 60 / 5 / countToAverageOn)
height = 500

def averagePoints(data):
    total = 0.0
    for dataPoint in data:
        total += dataPoint[1]
    return total / len(data)

weatherData = buildOrderedData("./seatac2019")
im = Image.new('RGBA', (width, height))
draw = ImageDraw.Draw(im)


for i in range(0, len(weatherData), countToAverageOn):
    opacity = averagePoints(weatherData[i:i+countToAverageOn])
    draw.line([(i/countToAverageOn,0),(i/countToAverageOn,height)], fill=(0,0,0, int(255 * opacity)), width=1)

im.show()