from pullData import buildOrderedData

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd


if __name__ == "__main__":
    weatherData = np.array(buildOrderedData("./seatac2019"))
    
    framedData = []
    for item in weatherData:
        dt = item[0]
        framedData.append((dt.timetuple().tm_yday, dt.hour * 60 + dt.minute, item[1]))
    
    df = pd.DataFrame(framedData, columns=["day", "minute", "opacity"])
    df = df.pivot_table(index='day', columns='minute', values='opacity')

    print(df)
    print(type(df).__name__)
    ax = sns.heatmap(df, cmap="Greys")
    plt.show()
