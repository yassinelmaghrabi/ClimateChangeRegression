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


class globaltemps:
    def __init__(self, degree=2, test_size=0.2):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(script_dir, 'data', 'GlobalTemperatures.csv')
        self.df = pd.read_csv(data_path)
        self.train(["dt"], deg=degree, test_size=test_size)

    def cleandata(self):
        self.df = self.df.dropna(subset=["LandAverageTemperature"])
        self.df = self.df[self.df['LandAverageTemperatureUncertainty'] <= 3]

    def preparedata(self):
        self.cleandata()
        self.df["dt"] = pd.to_datetime(self.df["dt"])
        self.df["dt"] = self.df["dt"].apply(lambda x: x.year)
        self.df = self.df.groupby("dt", as_index=False).mean()
        ransac = RANSACRegressor(random_state=0, residual_threshold=0.7)
        X = self.df["dt"].values.reshape(-1, 1)
        y = self.df["LandAverageTemperature"].values
        ransac.fit(X, y)
        inlier_mask = ransac.inlier_mask_
        # inlier_mask[-18:] = True
        self.dfo = self.df[~inlier_mask]
        self.df = self.df[inlier_mask]

    def split_data(self, features, target, test_size=0.2, random_state=None):
        test_size = float(test_size)
        X = self.df[features]
        y = self.df[target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        return X_train, X_test, y_train, y_test

    def train(self, features, target="LandAverageTemperature", deg=2, test_size=0.2, random_state=4):
        self.preparedata()
        model = Pipeline([('poly', PolynomialFeatures(degree=deg)),
                          ('linear', linear_model.LinearRegression(fit_intercept=False))])

        X_train, X_test, y_train, y_test = self.split_data(features, target, test_size=test_size,
                                                           random_state=random_state)
        self.model = model.fit(X_train, y_train)
        self.coef_ = model.named_steps['linear'].coef_
        self.y_pred = model.predict(X_test)
        self.X_test = X_test
        self.X_train = X_train
        self.y_train = y_train
        self.y_test = y_test
        self.msr_ = mean_squared_error(y_test, self.y_pred)
        self.r2_ = r2_score(y_test, self.y_pred)

    def predict(self, year):
        x_df = pd.DataFrame([year], columns=['dt'])
        val = self.model.predict(x_df)[0]
        return val

    def plot(self):
        x_min = np.min(self.X_test)
        x_max = np.max(self.X_test)
        x_values = np.linspace(x_min, x_max, 100)
        plt.scatter(self.X_test, self.y_test, color="black")
        plt.scatter(self.X_train, self.y_train, color="black", s=5)
        y_values = np.polyval(self.coef_[::-1], x_values)
        plt.plot(x_values, y_values, color="blue", linewidth=3)
        return plt

    def plotembed(self):
        x_min = np.min(self.X_train)
        x_max = np.max(self.X_train)
        x_values = np.linspace(x_min, x_max, 100)
        color_scale = np.interp(self.X_test.values.flatten(), [x_min, x_max], [0, 1])
        scatter_test = go.Scatter(
            x=self.X_test.values.flatten(),
            y=self.y_test.values.flatten(),
            mode='markers',
            marker=dict(color=np.interp(self.X_test.values.flatten(), [x_min, x_max], [0, 1]), colorscale='Viridis',
                        size=10),
            name='Test Data'
        )
        scatter_train = go.Scatter(
            x=self.X_train.values.flatten(),
            y=self.y_train.values.flatten(),
            mode='markers',
            marker=dict(color=np.interp(self.X_train.values.flatten(), [x_min, x_max], [0, 1]), colorscale='Viridis',
                        size=5),
            name='Train Data'
        )
        self.dfo
        scatter_out = go.Scatter(
            x=self.dfo.dt.values.flatten(),
            y=self.dfo.LandAverageTemperature.values.flatten(),
            mode='markers',
            marker=dict(color="red", size=3),
            name='Outliers'
        )

        # Polynomial curve plot
        y_values = np.polyval(self.coef_[::-1], x_values)
        polynomial_curve = go.Scatter(x=x_values, y=y_values, mode='lines', line=dict(color='white', width=3),
                                      name='Polynomial Curve')

        # Create figure
        fig = go.Figure([scatter_test, scatter_train, polynomial_curve, scatter_out])

        # Update layout
        fig.update_layout(
            title="Polynomial Regression Plot",
            xaxis_title="Year",
            yaxis_title="Temperature",
            template="plotly_dark"
        )

        return pio.to_html(fig, full_html=False)




