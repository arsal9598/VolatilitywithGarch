from flask import Flask, render_template, request
from models.garch_model import fetch_data, garch_fit_predict
from utils.data_processing import format_volatility
import plotly.graph_objects as go
import plotly
import json
import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    stock = "GOOG"
    start = "2020-01-01"
    end = datetime.date.today().strftime("%Y-%m-%d")
    forecast_range = None
    plot_data = None

    if request.method == "POST":
        stock = request.form.get("stock")  # Get the stock symbol from user input
        start = request.form.get("start")  # Get the start date from user input
        end = request.form.get("end")      # Get the end date from user input

        # Fetch data and fit GARCH model
        try:
            data = fetch_data(stock, start=start, end=end)
            data, forecast_vol = garch_fit_predict(data)

            # Format volatility forecast range
            forecast_range = format_volatility(forecast_vol)

            # Create the Plotly graph
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data.index, y=data['log_return'], mode='lines', name="Log Returns"))
            fig.add_trace(go.Scatter(x=data.index, y=data['fitted_vol'], mode='lines', name="Fitted Volatility", line=dict(color='red')))

            # Convert Plotly figure to JSON for rendering in the template
            plot_data = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        except Exception as e:
            forecast_range = f"Error fetching data: {str(e)}"

    return render_template("index.html", stock=stock, start=start, end=end, forecast_range=forecast_range, plot_data=plot_data)

if __name__ == "__main__":
    app.run(debug=True)