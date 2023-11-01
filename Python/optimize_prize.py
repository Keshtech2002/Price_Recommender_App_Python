import pandas as pd
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.formula.api import ols
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('Price.csv')
fig_PriceVsQuantity = px.scatter(df, x="Price", y="Quantity", trendline="ols")
fig_PriceVsQuantity.show()


def fun_optimize(var_opt, var_range, var_cost, df):
    """[summary]

    Args:
        var_opt ([string]): [The value will be either price or quantity based on the selection made from UI]
        var_range ([int]): [The value will be maximum & minimum price based on selection made from range slider from UI]
        var_cost ([type]): [This is the fixed cost entered from UI]
        df ([type]): [The data set for our usecase]

    Returns:
        [list]: [Returns a dataframe for table, 
                chart for Price Vs Quantity, 
                chart for optimized price set for maximum revenue, 
                Optimized value of revenue]
    """
    
    
    
    fig_PriceVsQuantity = px.scatter(df, x="Price", y="Quantity", color="Year", trendline="ols")
    """
    visualize the relationship between the 'Price' and 'Quantity' columns from the DataFrame 'df'. 
    The trendline="ols" option adds a trendline to the plot using ordinary least squares (OLS) regression.
    """
    
    # Fit OLS model
    model = ols("Quantity ~ Price", data=df).fit()
    
    Price = list(range(var_range[0], var_range[1], 10))
    cost = int(var_cost)
    quantity = []
    Revenue = []
    
    for i in Price:
        demand = model.params[0] + (model.params[1] * i)
        quantity.append(demand)
        Revenue.append((i-cost) * demand)
    """
    Calculate the quantity and revenue for a range of prices. 
    It iterates through the 'Price' values, calculates the demand using the regression model,
    and then calculates the revenue based on the difference between the price and cost.
    """
    
    # Create DataFrame
    profit = pd.DataFrame({"Price": Price, "Revenue": Revenue, "Quantity": quantity})
    
    # This line identifies the row in the 'profit' DataFrame where the revenue is maximum.
    max_val = profit.loc[(profit['Revenue'] == profit['Revenue'].max())]
    
    fig_PriceVsRevenue = go.Figure()
    fig_PriceVsRevenue.add_trace(go.Scatter(x=profit['Price'], y=profit['Revenue']))
    fig_PriceVsRevenue.add_annotation(x=int(max_val['Price']), y=int(max_val['Revenue']), text="Maximum Revenue", showarrow=True, arrowhead=1)
    fig_PriceVsRevenue.update_layout(showlegend=False, xaxis_title="Price", yaxis_title="Revenue")
    fig_PriceVsRevenue.add_vline(x=int(max_val['Price']), line_width=2, line_dash="dash", line_color="red", opacity=0.25)
    """
    A new Plotly figure 'fig_PriceVsRevenue' is created. 
    It's used to visualize the relationship between 'Price' and 'Revenue' 
    and highlights the point where revenue is maximized.
    """
    
    """
    returns a list containing the 'profit' DataFrame, 
    the 'fig_PriceVsRevenue' plot, 
    the 'fig_PriceVsQuantity' plot, 
    
    the optimized price, 
    the corresponding revenue value.
    """
    return [profit, fig_PriceVsRevenue, fig_PriceVsQuantity, round(max_val['Price'].values[0],2),round(max_val['Revenue'].values[0],3)]