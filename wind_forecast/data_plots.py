import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def wind_speed(pandas_df: object):
    ax = plt.gca()
    pandas_df.plt(
        kind="line",
        x="",
        y="",
        color="red",
        ax=ax,
    )
    plt.title("Wind Speed Line Plot")
    plt.xlabel("")
    plt.ylabel("")
    plt.show()


def wind_gust(pandas_df: object):
    pandas_df.plt(kind="scatter", x="", y="", color="red")
    plt.title("Wind Gust ScatterPlot")
    plt.xlabel("")
    plt.ylabel("")
    plt.show()


def wind_direction(pandas_df: object):

    pandas_df.plt(kind="scatter", x="", y="", color="red")
    plt.title("Wind Gust ScatterPlot")
    plt.xlabel("")
    plt.ylabel("")
    plt.show()
