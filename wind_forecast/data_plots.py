import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

class DisplayPlots():
    """class to plot wind values and display them in graphical depictions"""

    def wind_speed(self, merged_df: object):
        """plot to display wind speeds over time"""
        image = BytesIO()
        plt.plot([],[], color='y', label = 'Actual Wind Speed', linewidth=5)
        plt.plot([],[], color='g', label = 'Predicted Wind Speed', linewidth=5)
        plt.plot([],[],color = 'r', label='Actual Wind Gust', linewidth=5)
        plt.stackplot(
            merged_df["forecastForDateTime"],
            merged_df["readingWindSpeed"],
            merged_df["forecastWindSpeed10m"],
            merged_df["readingWindGust"],
            colors=[ 'y', 'g', 'r' ],
        )
        plt.title("Actual/Predicted Wind Speeds")
        plt.xlabel("Time")
        plt.ylabel("Wind Speed (MPH)")
        plt.legend()
        plt.savefig(image, format='png')
        return base64.encodebytes(image.getvalue())

    def wind_direction(self, pandas_df: object):
        """plot to display wind directions over time"""
        image = BytesIO()
        pandas_df.plot(
            kind="scatter",
            x="forecastForDateTime",
            y="forecastWindDirection10m",
            color="red"
        )
        plt.title("Wind Direction ScatterPlot")
        plt.xlabel("Time")
        plt.ylabel("Wind Direction")
        #plt.show()
        plt.plot()
        plt.savefig(image, format='png')
        return base64.encodebytes(image.getvalue())