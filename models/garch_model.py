import yfinance as yf
import numpy as np
import pandas as pd
from arch import arch_model

def fetch_data(ticker, start, end):
    """Fetch stock data from Yahoo Finance."""
    df = yf.download(ticker, start=start, end=end)
    df['log_return'] = np.log(df['Adj Close'] / df['Adj Close'].shift(1))
    df.dropna(inplace=True)
    return df

def garch_fit_predict(data, horizon=5):
    """Fit GARCH model and predict volatility."""
    returns = data['log_return']

    # Fit the GARCH(1,1) model
    am = arch_model(returns, mean="Zero", vol="Garch", p=1, q=1)
    res = am.fit(disp="off")

    # Forecast volatility
    forecasts = res.forecast(horizon=horizon)
    forecast_vol = np.sqrt(forecasts.variance.iloc[-1, :])
    
    # Get conditional volatility for past data
    data['fitted_vol'] = res.conditional_volatility

    return data, forecast_vol