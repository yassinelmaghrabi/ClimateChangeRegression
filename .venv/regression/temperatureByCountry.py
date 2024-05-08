import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from scipy import stats
import os
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.linear_model import RANSACRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score


class tempcountry:
    def __init__(self, country, cleaningthreshold=2.5, degree=2, test_size=0.2):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(script_dir,  'data', 'GlobalLandTemperaturesByCountry.csv')
        self.df = pd.read_csv(data_path)
        self.threshold = cleaningthreshold
        self.country = country
        self.train(["dt"], deg=degree, test_size=test_size)

    def show_info(self):
        print(self.df.info())

    def show_head(self, n=5):
        print(self.df.head(n))

    def describe(self):
        print(self.df.describe())

    def cleandata(self):
        self.df = self.df.dropna(subset=["AverageTemperature"])
        self.df=self.df[self.df['AverageTemperatureUncertainty'] <= 5]

    def preparedata(self):
        self.cleandata()
        self.df["dt"] = pd.to_datetime(self.df["dt"])
        self.df["dt"] = self.df["dt"].apply(lambda x: x.year)
        self.df = self.df.groupby("dt", as_index=False).mean()
        self.df = self.df[self.df['Country'] == self.country]  # Filter by country
        ransac = RANSACRegressor(random_state=0)
        X = self.df["dt"].values.reshape(-1, 1)
        y = self.df["AverageTemperature"].values
        ransac.fit(X, y)
        inlier_mask = ransac.inlier_mask_
        self.df = self.df[inlier_mask]
        min_temperatures = self.df[self.df['AverageTemperature'] == self.df['AverageTemperature'].min()] # find out min Temp
        print(min_temperatures)
        max_temperatures = self.df[self.df['AverageTemperature'] == self.df['AverageTemperature'].max()] # find out max Temp
        print(max_temperatures)

    def get_available_countries(self):
        country_counts = self.df['Country'].value_counts()
        countries = country_counts[country_counts > 1000].index.tolist()
        return countries