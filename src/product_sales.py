import pandas as pd
import numpy as np
import seaborn as sns

class prod_sales(object):
    '''
    Looks at perfomance of indiviudal products
    
    Inputs: 
        df = DataFrame containing sales data
        description = product in question
        (optional) month = subset by transaction month
        (optional) cluster = subset property_code cluster
        
    Produces a subsetted DataFrame of sales per property of that product
        
    Methods:
        return_df() : returns a DatFrame of the subsetted data
        plot_sales() :  returns number sold and revenue as a function of price
        plot_dists() : plots the distribution of price, number sold, and revenue
    '''
    
    def __init__(self, df, description, month = None, cluster = None):
        self.df = df
        self.description = description
        self.month = month
        self.cluster = cluster
        self.data = df[df.description == description]
        if cluster:
            self.data = df[df.cluster == cluster]
        self.data = self.data.groupby('unit_price').mean()[['number_sold']].reset_index()
        self.data['revenue'] = self.data.unit_price * self.data.number_sold
        
    def return_df(self):
        return self.data
    
    def plot_sales(self):
    
        if self.data.shape[0] < 2:
            return 'Not enough sales for selected product to plot'

        x = self.data['unit_price']
        y0 = self.data['number_sold']
        spl0 = UnivariateSpline(x, y0)
        spl0.set_smoothing_factor(1000000)
        y1 = self.data['revenue']
        spl1 = UnivariateSpline(x, y1)
        spl1.set_smoothing_factor(1000000)

        fig, ax = plt.subplots(1,2, figsize = (9,4))

        sns.scatterplot(x, y0, ax = ax[0])
        ax[0].set_xlabel('Unit Price')
        ax[0].set_ylabel('Average Number Sold')
        ax[0].plot(x, spl0(x), c = 'b', label='Spline Fit')
        ax[0].legend()
        sns.scatterplot(x, y1, ax = ax[1])
        ax[1].set_xlabel('Unit Price')
        ax[1].set_ylabel('Average Revenue')
        ax[1].plot(x, spl1(x), c = 'b', label='Spline Fit')
        ax[1].legend()
        if self.cluster:
            clust_descrip = ' | Cluster: {}'.format(self.cluster)
        else:
            clust_descrip = ''
        plt.suptitle(self.description + clust_descrip)
    
    def plot_dists(self):
        fig, ax = plt.subplots(1,3, figsize = (12,4))
        
        cols = list(self.data.columns)
            
        for i, col in enumerate(cols):
            ax[i] = sns.distplot(self.data[col], bins = 15, ax = ax[i])
            ax[i].set
            ax[i].set_title = col
        plt.tight_layout()