# referenced https://www.geeksforgeeks.org/graph-plotting-in-python-set-1/ for plotting examples
# as well as https://stackoverflow.com/questions/38061267/matplotlib-graphic-image-to-base64 for base64 conversion
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

class DisplayPlots:
    """class to plot wind values and display them in graphical depictions"""

    def wind_speed(self, merged_df: object):
        """plot to display wind speeds over time"""
        image = BytesIO()
        plt.plot([], [], color="y", label="Actual Wind Speed", linewidth=5)
        plt.plot([], [], color="g", label="Predicted Wind Speed", linewidth=5)
        plt.plot([], [], color="r", label="Actual Wind Gust", linewidth=5)
        plt.stackplot(
            merged_df["forecastForDateTime"],
            merged_df["readingWindSpeed"],
            merged_df["forecastWindSpeed10m"],
            merged_df["readingWindGust"],
            colors=["y", "g", "r"],
        )
        plt.title("Actual vs Predicted Wind Speeds")
        plt.xlabel("Time")
        plt.ylabel("Wind Speed (MPH)")
        plt.legend()
        plt.savefig(image, format="png")
        return base64.encodebytes(image.getvalue())

    def wind_direction(self, merged_df: object):
        """plot to display wind directions over time"""
        image = BytesIO()
        plt.plot([], [], color="g", label="Predicted Wind Direction", linewidth=5)
        plt.plot([], [], color="r", label="Actual Wind Direction", linewidth=5)
        plt.stackplot(
            merged_df["forecastForDateTime"],
            merged_df["forecastWindDirection10m"],
            merged_df["readingWindDirection"],
            colors=["g", "r"],
        )
        plt.title("Actual vs Predicted Wind Directions")
        plt.xlabel("Time")
        plt.ylabel("Wind Direction (degrees)")
        plt.legend()
        plt.savefig(image, format="png")
        return base64.encodebytes(image.getvalue())

    def wind_direction_diff(self, pandas_df: object):
        """plot to display difference in wind direction over time"""
        image = BytesIO()
        pandas_df.plot(
            kind="scatter", x="forecastForDateTime", y="windDirectionDiff", color="red"
        )
        plt.title("Wind Direction (degree difference from predicted)")
        plt.xlabel("Time")
        plt.ylabel("Wind Direction Difference")
        plt.plot()
        plt.savefig(image, format="png")
        return base64.encodebytes(image.getvalue())

    def wind_speed_diff(self, pandas_df: object):
        """plot to display difference in wind speed over time"""
        image = BytesIO()
        pandas_df.plot(
            kind="scatter", x="forecastForDateTime", y="windSpeedDiff", color="red"
        )
        plt.title("Wind Speed Difference from Predicted")
        plt.xlabel("Time")
        plt.ylabel("Wind Speed Difference")
        plt.plot()
        plt.savefig(image, format="png")
        return base64.encodebytes(image.getvalue())
