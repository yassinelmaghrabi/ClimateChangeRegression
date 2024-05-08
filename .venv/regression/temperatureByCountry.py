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
    def __init__(self,cleaningthreshold=2.5,degree=2,test_size=0.2):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(script_dir,  'data', 'GlobalLandTemperaturesByCountry.csv')
        self.df = pd.read_csv(data_path)
        self.threshold = cleaningthreshold
        self.train(["dt"],deg=degree,test_size=test_size)
        

    def show_info(self):
        print(self.df.info())

    def show_head(self, n=5):
        print(self.df.head(n))
    
    def describe(self):
        print(self.df.describe())

    def cleandata(self):
        self.df = self.df.dropna(subset=["AverageTemperature"])
        z_scores = np.abs(stats.zscore(self.df["AverageTemperature"]))
        self.df = self.df[(z_scores < self.threshold)]

    
    def preparedata(self):
        self.cleandata()
        self.df["dt"] = pd.to_datetime(self.df["dt"])
        self.df["dt"]=self.df["dt"].apply(lambda x : x.year)
        self.df = self.df.groupby("dt",as_index=False).mean()
        ransac = RANSACRegressor(random_state=0)
        X = self.df["dt"].values.reshape(-1, 1)
        y = self.df["AverageTemperature"].values
        ransac.fit(X, y)
        inlier_mask = ransac.inlier_mask_
        self.df = self.df[inlier_mask]
        print( inlier_mask)
        min_temperatures = self.df[self.df['AverageTemperature'] == self.df['AverageTemperature'].min()] #find out min Temp
        print(min_temperatures)
        max_temperatures = self.df[self.df['AverageTemperature'] == self.df['AverageTemperature'].max()] #find out max Temp
        print(max_temperatures)
        
    def split_data(self, features, target, test_size = 0.2, random_state = None):
        test_size = float(test_size)
        X=self.df[features]
        y=self.df[target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        return X_train, X_test, y_train, y_test

    def train(self, features, target='LandAverageTemperature', deg=2, test_size=0.2, random_state=None):    
        self.preparedata()
        model = Pipeline(['poly', PolynomialFeatures(degree=deg)),
                         ('Linear' , Linera_model.LinearRegression(fit_intercept=False))])
        X_train, X_test, y_train, y_tast=self.split_data(features,target,test_size=test_size,random_state=random_state)
        self.model =  model.fit(X_train, y-train)
        self.coef_ = model.named_steps['linear'].coef_
        self.y_pred = model.predict(X_test)
        seld.X_test = X_test
        self.X_train = X_train
        self.y_train = y_train
        self.y_test = y_test
        self.msr_ = mean_squared_error(y_test,self.y_pred)
        self.r2_ =r2_score(y_test,self.y_pred)
         
    def predict (self,year):
        x_df = pd.DataFrame([year], columns=['dt'])
        val = self.model.predict(x_df)[0]
        return val

    def plotembed(self):
        x_min = np.min(self.X_train)
        x_max = np.max(self.X_train)
        x_values = np.linspace(x_min, x_max, 100)
        color_scale = np.interp(self.X_test.values.flatten(),, [x_min, x_max], [0,1])
        scatter_test = go.Scatter(
            x=self.X_test.values.flatten(),
            y=self.y_test.values.flatten(),
            mode='markers',
            marker=dict(color=np.interp(self.X_test.values.flatten(), [x_min, x_max], [0,1]), colorscale='viridis', size=10),
            name='Test Data'
        )
        scatter_train = go.scatter(
            x=self.X_train.vlues.flatten(),
            y=self.y_train.values.flatten(),
            mode='markers',
            marker=dict(color=np.interp(self.X_test.values.flatten(), [x_min, x_max], [0,1]), colorscale='viridis', size=5),
            name='Train Data'
        )
        self.dfo
        scatter_out = go.Scatter(
            x=self.dfo.dt.values.flatten(),
            y=self.dfo.LandAverageTeperature.values.flatten(),
            mode='markers',
            marker=dict(color='red', size=3),
            name='Outliers'
        )
        y_values = np.polyval(self.coef_[::-1], x_values)
        plynomial_curve = go.Scatter(x=x_values, y=y_values, mode='Lines' , line=dict(color='white' ,width=3), name='Polynomial Curve')

        fig.update_layout(
            title='Plynomial Regression Plot',
            xaxis_title='X Values',
            yaxis_title='Y Values',
            template='plotly_dark'
        )

        return pio.to_html(fig,full_html=False) 
    
