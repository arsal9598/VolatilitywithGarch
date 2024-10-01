import numpy as np

def format_volatility(forecast_vol):
    """Format volatility forecast as a readable string."""
    vol_range = f"{round(min(forecast_vol), 4)} - {round(max(forecast_vol), 4)}"
    return vol_range